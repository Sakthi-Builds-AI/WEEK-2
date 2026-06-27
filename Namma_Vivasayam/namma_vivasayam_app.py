# ============================================================
#   NAMMA VIVASAYAM - Powered by SAKTHI AI
#   Your Smart Farming AI Assistant
#   Step 5: Streamlit Chat UI - Enhanced Design
# ============================================================

import os
import streamlit as st
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import io
from openai import OpenAI
import io

load_dotenv()

st.set_page_config(
    page_title="Namma Vivasayam | SAKTHI AI",
    page_icon="🌾",
    layout="centered"
)

st.markdown("""
<style>
    .header-box {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%);
        padding: 28px 24px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 16px;
    }
    .header-box h1 {
        color: white;
        font-size: 2em;
        margin: 8px 0 4px 0;
        font-weight: 600;
        letter-spacing: -0.3px;
    }
    .header-box p {
        color: #b7e4c7;
        font-size: 0.88em;
        margin: 4px 0 8px 0;
    }
    .powered-by {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        color: #d8f3dc;
        font-size: 0.75em;
        padding: 3px 14px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .stats-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-bottom: 16px;
    }
    .stat-box {
        background: #f0faf4;
        border: 1px solid #d8f3dc;
        border-radius: 10px;
        padding: 12px 10px;
        text-align: center;
    }
    .stat-num {
        font-size: 1.5em;
        font-weight: 600;
        color: #2d6a4f;
        line-height: 1.2;
    }
    .stat-label {
        font-size: 0.7em;
        color: #52b788;
        margin-top: 3px;
    }
    .lang-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 16px;
    }
    .lang-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 16px;
    }
    .lang-btn {
        padding: 10px;
        border-radius: 8px;
        border: 1.5px solid #d8f3dc;
        background: #f0faf4;
        color: #2d6a4f;
        font-size: 0.88em;
        text-align: center;
        font-weight: 500;
    }
    .lang-btn.active {
        border-color: #2d6a4f;
        background: #d8f3dc;
        color: #1b4332;
        font-weight: 600;
    }
    div[data-testid="stRadio"] {
        display: none !important;
    }
    .farmer-msg {
        background: #ffffff;
        border: 1px solid #d8f3dc;
        border-left: 4px solid #52b788;
        padding: 12px 16px;
        border-radius: 0 10px 10px 0;
        margin: 8px 0;
        color: #1b4332;
        font-size: 15px;
    }
    .bot-msg {
        background: #f0faf4;
        border: 1px solid #d8f3dc;
        border-left: 4px solid #2d6a4f;
        padding: 14px 16px;
        border-radius: 0 10px 10px 0;
        margin: 8px 0;
        color: #1b4332;
        font-size: 15px !important;
        line-height: 1.7;
    }
    .bot-msg h1, .bot-msg h2, .bot-msg h3,
    .bot-msg h4, .bot-msg h5, .bot-msg h6 {
        font-size: 15px !important;
        font-weight: 600 !important;
        margin: 8px 0 4px 0;
    }
    .bot-msg p, .bot-msg li {
        font-size: 15px !important;
    }
    .quick-label {
        font-size: 0.72em;
        font-weight: 600;
        color: #52b788;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.75em;
        margin-top: 24px;
        padding-top: 14px;
        border-top: 1px solid #e9ecef;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# Header with Shield Logo
st.markdown("""
<div class="header-box">
    <div style="width:64px;height:64px;margin:0 auto 10px auto;position:relative;">
        <div style="width:64px;height:64px;background:#081c15;border:2px solid #52b788;border-radius:4px 4px 32px 32px;display:flex;align-items:center;justify-content:center;clip-path:polygon(50% 0%, 100% 15%, 100% 60%, 50% 100%, 0% 60%, 0% 15%);">
            <span style="color:#d8f3dc;font-family:Georgia,serif;font-size:18px;font-weight:700;letter-spacing:2px;">NV</span>
        </div>
        <div style="position:absolute;top:6px;left:50%;transform:translateX(-50%);width:14px;height:14px;background:#f9c74f;border-radius:50%;"></div>
    </div>
    <h1>Namma Vivasayam</h1>
    <p>உங்கள் சிறந்த விவசாய AI உதவியாளர் &nbsp;·&nbsp; Your Smart Farming AI Assistant</p>
    <span class="powered-by">Powered by SAKTHI AI</span>
</div>
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-num">54</div>
        <div class="stat-label">Govt Schemes</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">2</div>
        <div class="stat-label">Languages</div>
    </div>
    <div class="stat-box">
        <div class="stat-num">24/7</div>
        <div class="stat-label">Available</div>
    </div>
</div>
""", unsafe_allow_html=True)
# Load Models
@st.cache_resource
def load_models():
    embedder      = SentenceTransformer("all-MiniLM-L6-v2")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    chroma_client = chromadb.PersistentClient(path="namma_vivasayam_db")
    collection    = chroma_client.get_or_create_collection(name="namma_schemes")
    return embedder, openai_client, collection

embedder, openai_client, collection = load_models()

# Language Toggle — hidden radio for state, custom HTML for display
lang = st.radio("lang", ["English", "Tamil"], horizontal=True, label_visibility="collapsed")

col_e, col_t = st.columns(2)
with col_e:
    if st.button("🇮🇳 English", use_container_width=True):
        st.session_state["lang_choice"] = "English"
        st.rerun()
with col_t:
    if st.button("🇮🇳 தமிழ்", use_container_width=True):
        st.session_state["lang_choice"] = "Tamil"
        st.rerun()

lang = st.session_state.get("lang_choice", "English")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    welcome = (
        "வணக்கம்! நான் நம்ம விவசாயம் AI உதவியாளர். TN அரசு விவசாய திட்டங்கள் பற்றி கேளுங்கள்!"
        if lang == "Tamil"
        else "Welcome! I am Namma Vivasayam AI Assistant. Ask me about TN Government farming schemes!"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="farmer-msg">👨‍🌾 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        clean = msg["content"].replace("##", "").replace("# ", "").replace("**", "")
        st.markdown(f'<div class="bot-msg">🌾 {clean}</div>', unsafe_allow_html=True)

# Quick Questions
st.markdown('<div class="quick-label">Quick Questions</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("🌱 Seed schemes?"):
        st.session_state.quick_q = "What seed schemes are available for farmers?"
    if st.button("💧 Water pipe subsidies?"):
        st.session_state.quick_q = "Are there any water pipe schemes for farmers?"
with col2:
    if st.button("🐛 Pest control schemes?"):
        st.session_state.quick_q = "What pest control schemes are available?"
    if st.button("📋 All schemes list"):
        st.session_state.quick_q = "List all Tamil Nadu farming schemes with their benefits and how to apply"

placeholder = "உங்கள் கேள்வியை இங்கே தட்டச்சு செய்யுங்கள்..." if lang == "Tamil" else "Type your farming question here..."

# Voice Input
st.markdown("🎤 **Speak your question:**")
audio_input = st.audio_input("Record your farming question", label_visibility="collapsed")

# Transcribe voice if recorded
if audio_input is not None:
    with st.spinner("🎤 Transcribing your voice..."):
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", audio_input, "audio/wav"),
        )
    user_input = transcript.text
    st.info(f"🎤 You said: **{user_input}**")
else:
    # Text input
    col_input, col_btn = st.columns([8, 1])
    with col_input:
        user_input = st.text_input("", placeholder=placeholder, label_visibility="collapsed", key="user_input_box")
    with col_btn:
        send = st.button("➤", use_container_width=True)
    if not send:
        user_input = None

if "quick_q" in st.session_state:
    user_input = st.session_state.quick_q
    del st.session_state.quick_q

# RAG Function
def get_answer(question, language):
    # Translate Tamil question to English for better DB search
    tamil_chars = any('\u0b80' <= c <= '\u0bff' for c in question)
    if tamil_chars:
        translation = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Translate this Tamil text to English in one line: {question}"}],
            max_tokens=100
        )
        search_query = translation.choices[0].message.content
    else:
        search_query = question

    query_vector = embedder.encode(search_query).tolist()

    is_all_schemes = any(word in question.lower() for word in [
        "all schemes", "list all", "all welfare", "என்ன திட்டங்கள்", "அனைத்து திட்டங்கள்"
    ])
    n = 20 if is_all_schemes else 10

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n,
        include=["metadatas", "documents"]
    )
    context_chunks = [m["text"] for m in results["metadatas"][0]]
    context = "\n\n---\n\n".join(context_chunks)

    tamil_chars = any('\u0b80' <= c <= '\u0bff' for c in question)
    if tamil_chars or language == "Tamil":
        lang_instruction = "Answer in Tamil language only. Use simple Tamil words."
    else:
        lang_instruction = "Answer in clear simple English."

    prompt = (
        "You are Namma Vivasayam, an expert AI assistant for Tamil Nadu farmers.\n"
        "Powered by SAKTHI AI. You know every TN Government welfare scheme in detail.\n\n"
        + lang_instruction + "\n\n"
        "IMPORTANT RULES:\n"
        "1. Read the farmer question CAREFULLY and answer ONLY what they asked\n"
        "2. Do NOT list all schemes — only the ones DIRECTLY relevant to the question\n"
        "3. For each relevant scheme give:\n"
        "   Scheme Name\n"
        "   What is it: (2-3 simple sentences)\n"
        "   Who can apply: (eligibility clearly)\n"
        "   What you get: (exact benefit, subsidy amount if mentioned)\n"
        "   How to apply: (clear steps)\n"
        "   --------\n"
        "4. If question is about a SPECIFIC crop or topic, focus ONLY on that\n"
        "5. Use simple language a village farmer can understand\n"
        "6. Still summarize whatever relevant information you found in the context\n"
        "7. Do NOT make up any information — only use what is in the Context\n"
        "8. If English end with: For more info: www.tn.gov.in\n"
        "   If Tamil end with: மேலும் தகவலுக்கு: www.tn.gov.in\n\n"
        "Context from TN Government Schemes:\n" + context +
        "\n\nFarmer Question: " + question +
        "\n\nDetailed Answer:"
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Namma Vivasayam, a helpful Tamil Nadu farming assistant. "
                    "Always give specific, accurate, complete answers based only on the context provided."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )
    return response.choices[0].message.content

# Handle Input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="farmer-msg">👨‍🌾 {user_input}</div>', unsafe_allow_html=True)

    with st.spinner("🌾 Finding best schemes for you..."):
        answer = get_answer(user_input, lang)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    clean_answer = answer.replace("##", "").replace("# ", "").replace("**", "")
    st.markdown(f'<div class="bot-msg">🌾 {clean_answer}</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    🌾 Namma Vivasayam &nbsp;·&nbsp; Powered by SAKTHI AI &nbsp;·&nbsp; Data: Tamil Nadu Government &mdash; www.tn.gov.in
</div>
""", unsafe_allow_html=True)