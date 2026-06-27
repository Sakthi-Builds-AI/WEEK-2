"""
LangChain + LangSmith Tracing Assignment
-----------------------------------------
Sends a prompt to an OpenAI chat model via LangChain and prints the response.
Every run is automatically traced in the LangSmith dashboard.

Keys are loaded from a .env file in the same folder as this script.
Create a file named .env with the following contents:

    OPENAI_API_KEY=sk-...
    LANGCHAIN_API_KEY=ls__...
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_PROJECT=langchain-assignment

⚠️  Add .env to your .gitignore — never commit API keys.

Usage:
    python main.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ── 0. Load .env from the same folder as this script ─────────────────────────

env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    print(f"\n❌  No .env file found at: {env_path}")
    print("    Create one with your API keys. See the docstring at the top of this file.\n")
    sys.exit(1)

load_dotenv(dotenv_path=env_path)

# ── 1. Validate required environment variables ────────────────────────────────

REQUIRED_ENV_VARS = {
    "OPENAI_API_KEY": "Get yours at https://platform.openai.com/api-keys",
    "LANGCHAIN_API_KEY": "Get yours at https://smith.langchain.com",
    "LANGCHAIN_TRACING_V2": 'Must be set to "true" to enable LangSmith tracing',
    "LANGCHAIN_PROJECT": 'Name your project, e.g. "langchain-assignment"',
}

missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing:
    print("\n❌  Missing environment variables — please set them before running:\n")
    for var in missing:
        print(f"   {var}")
        print(f"     → {REQUIRED_ENV_VARS[var]}\n")
    sys.exit(1)

# ── 2. Imports (after env check so errors are clear) ──────────────────────────

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# ── 3. Build the model ────────────────────────────────────────────────────────

llm = ChatOpenAI(
    model="gpt-4o-mini",   # affordable, fast chat model
    temperature=0.7,
)

# ── 4. Define the prompt ──────────────────────────────────────────────────────

USER_PROMPT = "Tell me a fun fact about Tamil Nadu."

messages = [
    SystemMessage(content="You are a helpful and enthusiastic assistant."),
    HumanMessage(content=USER_PROMPT),
]

# ── 5. Send to OpenAI and print the result ────────────────────────────────────

print("\n" + "=" * 55)
print(f"Input:  {USER_PROMPT}")
print("=" * 55)

response = llm.invoke(messages)

print(f"\nOutput: {response.content}")
print("\n" + "=" * 55)
print("✅  Run logged to LangSmith project:", os.getenv("LANGCHAIN_PROJECT"))
print("    View at: https://smith.langchain.com")
print("=" * 55 + "\n")