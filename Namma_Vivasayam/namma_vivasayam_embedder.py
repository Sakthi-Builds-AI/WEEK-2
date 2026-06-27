# ============================================================
#   NAMMA VIVASAYAM - Powered by SAKTHI AI
#   Step 2 & 3: Rebuilding ChromaDB with pure SentenceTransformer
# ============================================================

import chromadb
from sentence_transformers import SentenceTransformer
from namma_vivasayam_loader import load_tn_schemes
import os
import shutil

CHROMA_PATH = "namma_vivasayam_db"
COLLECTION  = "namma_schemes"
EMBED_MODEL = "all-MiniLM-L6-v2"

def build_vector_db():
    print("🌾 Namma Vivasayam | SAKTHI AI")
    print("=" * 55)
    print("📄 Loading & chunking scheme data...")

    raw_blocks = load_tn_schemes()

    # Manual chunking — split long blocks into 600 char chunks
    chunks = []
    for block in raw_blocks:
        if len(block) <= 600:
            chunks.append(block)
        else:
            # split into overlapping chunks
            for i in range(0, len(block), 450):
                chunk = block[i:i+600]
                if len(chunk) > 80:
                    chunks.append(chunk)

    print(f"✅ Total chunks created: {len(chunks)}")

    # Load embedding model
    print("\n🔢 Loading SentenceTransformer model...")
    embedder = SentenceTransformer(EMBED_MODEL)

    # Generate embeddings
    print("🔢 Generating embeddings for all chunks...")
    embeddings = embedder.encode(chunks, show_progress_bar=True).tolist()

    # Clear old DB
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("🗑️  Cleared old ChromaDB")

    # Build fresh ChromaDB
    client     = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.create_collection(name=COLLECTION)

    # Store in batches of 50
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch_docs  = chunks[i:i+batch_size]
        batch_embs  = embeddings[i:i+batch_size]
        batch_ids   = [f"chunk_{i+j}" for j in range(len(batch_docs))]
        collection.add(
            documents=batch_ids,
            embeddings=batch_embs,
            ids=batch_ids,
            metadatas=[{"text": doc} for doc in batch_docs]
        )

    print(f"\n✅ ChromaDB rebuilt at ./{CHROMA_PATH}/")
    print(f"   Collection: {COLLECTION}")
    print(f"   Total vectors: {collection.count()}")
    print("\n🌾 Knowledge base READY! 🚜")

if __name__ == "__main__":
    build_vector_db()