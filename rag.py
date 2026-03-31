import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Globals
documents = []
index = None

# Files
INDEX_FILE = "faiss_index.bin"
DOC_FILE = "documents.pkl"


# -----------------------------
# SAVE / LOAD
# -----------------------------
def save_index():
    global index, documents

    if index is not None:
        faiss.write_index(index, INDEX_FILE)

        with open(DOC_FILE, "wb") as f:
            pickle.dump(documents, f)

        print("✅ Index saved")


def load_index():
    global index, documents

    try:
        index = faiss.read_index(INDEX_FILE)

        with open(DOC_FILE, "rb") as f:
            documents = pickle.load(f)

        print("✅ Index loaded")
        return True

    except:
        print("❌ No saved index found")
        return False


# -----------------------------
# TEXT CHUNKING
# -----------------------------
def chunk_text(text, chunk_size=800, overlap=100):
    if not text:
        return []

    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])

    return chunks


# -----------------------------
# BUILD INDEX
# -----------------------------
def build_index(all_contracts):
    global index, documents

    documents = []
    embeddings = []

    for contract_id, text in all_contracts:
        print("Processing contract:", contract_id)

        if not text or text.strip() == "":
            print("Skipping empty text")
            continue

        chunks = chunk_text(text)

        print("Chunks created:", len(chunks))

        for chunk in chunks:
            documents.append({
                "contract_id": contract_id,
                "text": chunk
            })
            embeddings.append(model.encode(chunk))

    # 🚨 Critical safety check BEFORE conversion
    if len(embeddings) == 0:
        print("❌ No embeddings created. Check your data.")
        index = None
        return

    embeddings = np.array(embeddings).astype('float32')

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    print("✅ Index built with", len(documents), "chunks")


# -----------------------------
# SEARCH
# -----------------------------
def search(query, k=3):
    global index, documents

    if index is None:
        print("❌ Index not built")
        return []

    query_embedding = model.encode([query]).astype('float32')

    distances, indices = index.search(query_embedding, k)

    results = []
    for idx in indices[0]:
        if idx < len(documents):
            results.append(documents[idx])

    return results