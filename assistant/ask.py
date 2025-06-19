from openai import OpenAI
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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant answering questions about company SOPs for One-Touch Automation based in Westfield, Indiana."
            },
            {
                "role": "user",
                "content": f"Answer this based on SOPs:\n{context}\n\nQuestion: {query}"
            }
        ]
    )

    return response.choices[0].message.content, sources
