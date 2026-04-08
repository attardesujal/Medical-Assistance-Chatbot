import os, argparse, glob, sys
from uuid import uuid4
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import requests

# ------------ Env & Config ------------
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX   = os.getenv("PINECONE_INDEX", "rag-docs")
PINECONE_HOST    = os.getenv("PINECONE_HOST")

EMBED_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
CHUNK_SIZE       = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP    = int(os.getenv("CHUNK_OVERLAP", "200"))

if not PINECONE_API_KEY or not PINECONE_HOST:
    print("ERROR: Pinecone config missing"); sys.exit(1)

# ------------ Clients ------------
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host=PINECONE_HOST)

embedder = SentenceTransformer(EMBED_MODEL_NAME)

def embed_texts(texts):
    return embedder.encode(texts, normalize_embeddings=True).tolist()

# ------------ OLLAMA LLM ------------
def call_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
    except Exception as e:
        return f"Ollama Error: {str(e)}"

# ------------ Core Logic ------------
def read_pdfs(folder):
    docs = []
    for path in glob.glob(os.path.join(folder, "*.pdf")):
        reader = PdfReader(path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            docs.append({
                "source": os.path.basename(path),
                "page": i+1,
                "text": text
            })
    return docs

def chunk_text(text):
    chunks, start = [], 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(end - CHUNK_OVERLAP, end)
    return chunks

def ingest(data_dir):
    docs = read_pdfs(data_dir)

    if not docs:
        print("No PDFs found."); return

    all_chunks = []
    for d in docs:
        for ch in chunk_text(d["text"]):
            all_chunks.append({
                "text": ch,
                "source": d["source"],
                "page": d["page"]
            })

    print(f"Chunks to upsert: {len(all_chunks)}")

    vectors = embed_texts([x["text"] for x in all_chunks])

    items = [{
        "id": str(uuid4()),
        "values": v,
        "metadata": x
    } for x, v in zip(all_chunks, vectors)]

    for i in range(0, len(items), 100):
        index.upsert(vectors=items[i:i+100])

    print(f"Upserted {len(items)} vectors to '{PINECONE_INDEX}'")
    print("✅ Ingestion complete")

# ------------ Query ------------

SYSTEM = ("You are a helpful AI assistant. Answer ONLY using the given context. "
          "If not found, say you don't know.")

def build_context(question, k=5):
    qvec = embed_texts([question])[0]
    res = index.query(vector=qvec, top_k=k, include_metadata=True)

    context_blocks = []
    sources = set()

    for m in res.matches:
        meta = m.metadata
        context_blocks.append(meta["text"])
        sources.add(f"{meta['source']} (page {meta['page']})")

    context = "\n\n".join(context_blocks)
    sources_text = "\n".join(sources)

    return context, sources_text

def ask(question, k=5, debug=False):
    context, sources = build_context(question, k)

    if debug:
        print("\n[DEBUG] --- Retrieved Context ---\n")
        print(context[:1500])

    if not context.strip():
        return "No relevant context found."

    prompt = f"""
{SYSTEM}

Answer in 3-4 lines maximum.
Be clear and concise.

Context:
{context}

Question:
{question}

Answer:
"""

    answer = call_ollama(prompt)

    final_output = f"""
========================================
FINAL ANSWER
========================================

{answer.strip()}

Sources:
{sources}

========================================
"""

    return final_output

# ------------ API ------------
def run_api(port):
    from fastapi import FastAPI
    from pydantic import BaseModel
    import uvicorn

    app = FastAPI()

    class Query(BaseModel):
        question: str
        k: int = 5

    @app.post("/ask")
    def get_answer(q: Query):
        return {"answer": ask(q.question, q.k)}

    uvicorn.run(app, host="0.0.0.0", port=port)

# ------------ CLI ------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["ingest", "ask", "api"])
    parser.add_argument("--data", default=".")
    parser.add_argument("--q", default="")
    parser.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    if args.mode == "ingest":
        ingest(args.data)

    elif args.mode == "ask":
        print(ask(args.q))

    elif args.mode == "api":
        run_api(args.port)
