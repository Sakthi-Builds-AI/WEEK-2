# 🌾 Namma Vivasayam
### Your Smart Farming AI Assistant | Powered by SAKTHI AI

Namma Vivasayam is a RAG-based AI assistant built for Tamil Nadu farmers. It reads real government scheme data from tn.gov.in and answers farmer questions in Tamil or English — through a web app, voice input and WhatsApp.

---

## What It Does

- Farmers can ask questions in **English or Tamil**
- **Voice input** — speak your question, Whisper transcribes it automatically
- **WhatsApp bot** — farmers can use without opening a browser
- Covers **54 Tamil Nadu Government farming schemes** with full details

---

## Tech Stack

| Layer | Tool |
|---|---|
| Web Scraping | Playwright + BeautifulSoup |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| Vector DB | ChromaDB (local) |
| LLM | OpenAI GPT-4o |
| Web UI | Streamlit |
| Voice | OpenAI Whisper |
| WhatsApp | Twilio + FastAPI |
| Tunnel | Ngrok |
| Language | Python 3.14 |

---

## Project Structure

```
Namma_Vivasayam/
├── namma_vivasayam_loader.py      ← Scrapes TN Gov website using Playwright
├── namma_vivasayam_embedder.py    ← Splits text and stores vectors in ChromaDB
├── namma_vivasayam_rag.py         ← RAG chain for terminal testing
├── namma_vivasayam_app.py         ← Streamlit web app with voice input
├── namma_vivasayam_whatsapp.py    ← WhatsApp bot via Twilio + FastAPI
├── requirements.txt               ← Python dependencies
└── .env.example                   ← Environment variables template
```

---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/shrisakthiselvaraj/namma-vivasayam.git
cd namma-vivasayam
```

### 2. Create virtual environment
```bash
python -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your API keys

### 5. Build the knowledge base
```bash
python namma_vivasayam_loader.py
python namma_vivasayam_embedder.py
```

### 6. Run the web app
```bash
streamlit run namma_vivasayam_app.py
```

### 7. Run the WhatsApp bot
```bash
python namma_vivasayam_whatsapp.py
```

---

## Environment Variables

Create a `.env` file with these keys:

```
OPENAI_API_KEY=your_openai_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
NGROK_AUTH_TOKEN=your_ngrok_token
```

---

## How It Works

1. **Playwright scraper** visits all 54 scheme pages on tn.gov.in and extracts full content
2. **HuggingFace embedder** converts scheme text into vectors
3. **ChromaDB** stores vectors locally for fast semantic search
4. **RAG Chain** finds top 10 matching schemes and sends to GPT-4o
5. **Tamil questions** are auto-translated to English for better DB search
6. **Streamlit UI** displays answers with Tamil/English language toggle
7. **Whisper** transcribes voice questions in Tamil or English
8. **WhatsApp bot** lets farmers get answers by just sending a message

---

## Data Source

Tamil Nadu Government — www.tn.gov.in

---

## Built By

**Shrisakthi Selvaraj**
Gen AI Architect Program — Social Eagle
Powered by SAKTHI AI
