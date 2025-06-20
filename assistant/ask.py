from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.Client(Settings(persist_directory="vectorstore", anonymized_telemetry=False))
collection = chroma_client.get_or_create_collection(name="sops")

def ask_ai(query):
    results = collection.query(
        query_texts=[query],
        n_results=4
    )

    chunks = results['documents'][0]
    sources = results['metadatas'][0]
    context = "\n\n".join(chunks)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly detailed and reliable assistant trained on official One-Touch Automation SOPs. When asked about how to install, configure, or build something, you must respond with a very specific list of steps. Always extract and include detailed tool names (e.g., cable crimper, laser level), cable or wire types (e.g., CAT6, HDMI, speaker wire), measurements (e.g., 18 inches from floor, 2 feet spacing), and mounting hardware or equipment models mentioned in the SOPs. Your goal is to make sure a technician could perform the job correctly just by reading your response. Respond with clear formatting using numbered steps or bulleted lists. Never respond vaguely. If you cannot find an exact answer in the SOPs, say 'not found in current SOPs.'"

                },
                {
                    "role": "user",
                    "content": f"Answer this based on SOPs:\n{context}\n\nQuestion: {query}"
                }
            ]
        )
        return response.choices[0].message.content, sources
    except OpenAIError as e:
        return f"⚠️ OpenAI API Error: {str(e)}", sources
