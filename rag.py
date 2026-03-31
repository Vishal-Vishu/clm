import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import traceback

model = SentenceTransformer('all-MiniLM-L6-v2')

# Store chunks + metadata
documents = []
index = None


def chunk_text(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks


def build_index(all_contracts):
    global index, documents

    documents = []
    embeddings = []

    for contract_id, text in all_contracts:
        chunks = chunk_text(text)

        for chunk in chunks:
            documents.append({
                "contract_id": contract_id,
                "text": chunk
            })
            embeddings.append(model.encode(chunk))

    embeddings = np.array(embeddings).astype('float32')

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)


def search(query, k=3):
    global index, documents

    if index is None:
        print("❌ Index not built yet")
        return []
    
    print("Query from user =",query)

    query_embedding = model.encode([query]).astype('float32')

    print("Query Embedding=", query_embedding)

    distances, indices = index.search(query_embedding, k)

    results = []
    for idx in indices[0]:
        try:
            if idx < len(documents):
                results.append(documents[idx])
        except Exception as e:
            print("An exception occurred, here is the stack trace:")
            traceback.print_exc() 
        

    print("Results = ", results)            

    return results