from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
import signal

class TimeoutException(Exception):
    pass

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.Client(Settings(persist_directory="vectorstore", anonymized_telemetry=False))
collection = chroma_client.get_or_create_collection(name="sops")

def handler(signum, frame):
    raise TimeoutException()

signal.signal(signal.SIGALRM, handler)

def ask_ai(query):
    results = collection.query(
        query_texts=[query],
        n_results=4
    )

    chunks = results['documents'][0]
    sources = results['metadatas'][0]
    context = "\n\n".join(chunks)

    try:
        signal.alarm(10)  # timeout after 10 seconds
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant answering questions about company SOPs for One-Touch Automation based in Westfield, Indiana. Your answers should be concise and descriptive. If you are stating answers that are in a bulleted list or numbered list format from the SOP then respond in a way that is effective. You are a helpful assistant for One-Touch Automation technicians. Always respond with clear, numbered steps or bullet points when procedures are asked for. Do not return long unstructured paragraphs. Use formatting like:\n\n 1. Step One\n2. Step Two\n\nor\n\n• Item One\n• Item Two.\n If you don’t know the answer from SOPs, say so clearly. Use simple language for technicians on-site. Highlight any safety warnings."
                },
                {
                    "role": "user",
                    "content": f"Answer this based on SOPs:\n{context}\n\nQuestion: {query}"
                }
            ]
        )
        signal.alarm(0)  # disable alarm after success
        return response.choices[0].message.content, sources
    except TimeoutException:
        return "⚠️ The assistant took too long to respond. Please try again later.", sources
    except OpenAIError as e:
        return f"⚠️ OpenAI API Error: {str(e)}", sources