# ============================================================
#   NAMMA VIVASAYAM - Powered by SAKTHI AI
#   Step 7: WhatsApp Bot via Twilio + FastAPI + Ngrok
# ============================================================

import os
import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from pyngrok import ngrok
import uvicorn
import threading

load_dotenv()

# ── Config ───────────────────────────────────────────────────
CHROMA_PATH = "namma_vivasayam_db"
COLLECTION  = "namma_schemes"
EMBED_MODEL = "all-MiniLM-L6-v2"

# ── Load Models ──────────────────────────────────────────────
print("🌾 Namma Vivasayam WhatsApp Bot | SAKTHI AI")
print("Loading models...")

embedder      = SentenceTransformer(EMBED_MODEL)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection    = chroma_client.get_or_create_collection(name=COLLECTION)

print(f"✅ ChromaDB loaded — {collection.count()} vectors")

app = FastAPI()

# ── RAG Function ─────────────────────────────────────────────
def get_whatsapp_answer(question):
    query_vector   = embedder.encode(question).tolist()

    # Detect if all schemes query
    is_all = any(w in question.lower() for w in [
        "all schemes", "list all", "all welfare",
        "என்ன திட்டங்கள்", "அனைத்து திட்டங்கள்"
    ])
    n = 15 if is_all else 8

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n,
        include=["metadatas"]
    )
    context_chunks = [m["text"] for m in results["metadatas"][0]]
    context        = "\n\n---\n\n".join(context_chunks)

    # Auto detect Tamil
    tamil_chars = any('\u0b80' <= c <= '\u0bff' for c in question)
    lang = "Tamil" if tamil_chars else "English"

    lang_instruction = (
        "Answer in Tamil. Use simple Tamil words."
        if lang == "Tamil"
        else "Answer in simple English."
    )

    prompt = (
        "You are Namma Vivasayam, a WhatsApp farming assistant powered by SAKTHI AI.\n"
        "You help Tamil Nadu farmers via WhatsApp. Keep answers SHORT and clear.\n\n"
        + lang_instruction + "\n\n"
        "Rules:\n"
        "1. Answer ONLY what was asked\n"
        "2. Keep total reply under 300 words (WhatsApp limit)\n"
        "3. For each scheme use this format:\n"
        "   *Scheme Name*\n"
        "   What: (1 sentence)\n"
        "   Who: (eligibility)\n"
        "   Benefit: (exact amount)\n"
        "   Apply: (where to go)\n"
        "   ---\n"
        "4. Use *bold* for scheme names (WhatsApp markdown)\n"
        "5. End with: www.tn.gov.in\n\n"
        "Context:\n" + context +
        "\n\nFarmer Question: " + question +
        "\n\nShort Answer:"
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful Tamil Nadu farming assistant. Be concise for WhatsApp."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )
    return response.choices[0].message.content

# ── WhatsApp Webhook ─────────────────────────────────────────
@app.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    question = Body.strip()
    print(f"\n📱 Message from {From}: {question}")

    # Greeting handler
    greetings = ["hi", "hello", "வணக்கம்", "help", "start", "helo"]
    if question.lower() in greetings:
        answer = (
            "🌾 *Namma Vivasayam* — Powered by SAKTHI AI\n\n"
            "Welcome! I help Tamil Nadu farmers find government schemes.\n\n"
            "Ask me anything like:\n"
            "• What seed schemes are available?\n"
            "• How to get gypsum subsidy?\n"
            "• விவசாயிகளுக்கு என்ன திட்டங்கள்?\n\n"
            "Type your question in English or Tamil!"
        )
    else:
        answer = get_whatsapp_answer(question)

    print(f"🌾 Answer: {answer[:100]}...")

    resp = MessagingResponse()
    resp.message(answer)
    return str(resp)

@app.get("/")
async def root():
    return {"status": "Namma Vivasayam WhatsApp Bot is running!"}

# ── Start Server + Ngrok ─────────────────────────────────────
if __name__ == "__main__":
    # Start ngrok tunnel
    print("\n🔗 Starting ngrok tunnel...")
    ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))
    http_tunnel = ngrok.connect(8000)
    public_url  = http_tunnel.public_url

    print(f"\n{'='*55}")
    print(f"✅ NAMMA VIVASAYAM WHATSAPP BOT LIVE!")
    print(f"{'='*55}")
    print(f"🌐 Public URL: {public_url}")
    print(f"📱 Webhook URL: {public_url}/whatsapp")
    print(f"\n👉 Copy this webhook URL and paste in Twilio:")
    print(f"   {public_url}/whatsapp")
    print(f"{'='*55}\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)