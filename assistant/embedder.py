import openai
from chromadb import PersistentClient
from dotenv import load_dotenv
import os
from assistant.load_pdfs import extract_text_from_pdf

load_dotenv()
openai.ai_key = os.getenv("OPENAI_API_KEY")

# set up chroma vector DB
chroma_client = PersistentClient(path="vectorstore") #vectorstore = local folder

def chunk_text(text, chunk_size=1250):
    #split long text into smaller parts
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def build_vector_store():
    docs = extract_text_from_pdf("data/")
    collection = chroma_client.get_or_create_collection(name="sops")

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            print(f"Adding chunk from {doc['filename']}...")
            collection.add(
                documents=[chunk],
                metadatas=[{"source" : doc["filename"]}],
                ids=[f"{doc['filename']}_{i}"]
            )

if __name__ == "__main__":
    build_vector_store()