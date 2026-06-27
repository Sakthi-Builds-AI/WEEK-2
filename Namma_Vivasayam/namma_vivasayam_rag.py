# NAMMA VIVASAYAM - Powered by SAKTHI AI
# Your Smart Farming AI Assistant
# Step 4: RAG Chain

import os
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI

load_dotenv()

CHROMA_PATH = "namma_vivasayam_db"
EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION = "langchain"

embedder = SentenceTransformer(EMBED_MODEL)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name=COLLECTION)

def ask_namma_vivasayam(question):
    print("\n" + "=" * 55)
    print("Farmer asks: " + question)
    print("-" * 55)

    query_vector = embedder.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=8
    )
    context_chunks = results["documents"][0]
    context = "\n\n".join(context_chunks)

    prompt = (
        "You are Namma Vivasayam, a smart farming AI assistant powered by SAKTHI AI.\n"
        "You help Tamil Nadu farmers understand government welfare schemes.\n\n"
        + lang_instruction + "\n\n"
        "Rules:\n"
        "- Give COMPLETE and DETAILED information about every scheme found\n"
        "- Format each scheme like this:\n"
        "  SCHEME NAME\n"
        "  What is it: (explain in 2-3 simple sentences)\n"
        "  Who can apply: (eligibility)\n"
        "  What you get: (benefit amount or item)\n"
        "  How to apply: (steps if available)\n"
        "  ---\n"
        "- Use simple words a village farmer understands\n"
        "- Do NOT say 'refer to website' — give ALL details from context\n"
        "- Do NOT cut short — give full information for every scheme\n"
        "- Only at the very end write: மேலும் தகவலுக்கு: www.tn.gov.in\n\n"
        "Context from TN Government Schemes:\n" + context + "\n\n"
        "Farmer Question: " + question + "\n\n"
        "Answer with FULL details:"
    )

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    answer = response.choices[0].message.content
    print("Namma Vivasayam:\n" + answer)
    print("\nRetrieved " + str(len(context_chunks)) + " scheme blocks")
    print("=" * 55)
    return answer

if __name__ == "__main__":
    print("NAMMA VIVASAYAM | SAKTHI AI")
    print("Your Smart Farming AI Assistant")
    print("=" * 55)

    ask_namma_vivasayam("What seed schemes are available for farmers?")
    ask_namma_vivasayam("விவசாயிகளுக்கு என்ன திட்டங்கள் உள்ளன?")