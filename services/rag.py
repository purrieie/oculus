import json
import os
from sentence_transformers import SentenceTransformer
import chromadb

_techniques = []
_model = None
_collection = None

def get_model():
    global _model
    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model loaded")
    return _model

def get_collection():
    global _collection
    if _collection is not None:
        return _collection
    client = chromadb.PersistentClient(path="./chroma_db")
    _collection = client.get_or_create_collection("oculus_kb")
    if _collection.count() == 0:
        print("Ingesting knowledge base into ChromaDB...")
        _ingest(_collection)
    else:
        print(f"ChromaDB already has {_collection.count()} chunks")
    return _collection

def _ingest(collection):
    model = get_model()
    docs, ids, metas = [], [], []

    # Ingest MITRE techniques
    load_mitre()
    for i, t in enumerate(_techniques):
        text = f"{t['id']} {t['name']}: {t['description']}"
        docs.append(text)
        ids.append(f"mitre_{i}")
        metas.append({"source": "mitre", "id": t["id"], "name": t["name"]})

    # Ingest in batches
    batch = 500
    for i in range(0, len(docs), batch):
        embeddings = model.encode(docs[i:i+batch]).tolist()
        collection.add(
            documents=docs[i:i+batch],
            embeddings=embeddings,
            ids=ids[i:i+batch],
            metadatas=metas[i:i+batch]
        )
        print(f"Ingested {min(i+batch, len(docs))}/{len(docs)} chunks")

def load_mitre():
    global _techniques
    if _techniques:
        return
    path = "data/mitre_attack.json"
    if not os.path.exists(path):
        print("MITRE JSON not found")
        return
    with open(path) as f:
        data = json.load(f)
    for obj in data.get("objects", []):
        if obj.get("type") == "attack-pattern" and not obj.get("revoked"):
            ext = obj.get("external_references", [])
            tid = next((e["external_id"] for e in ext if e.get("source_name") == "mitre-attack"), "")
            _techniques.append({
                "id": tid,
                "name": obj.get("name", ""),
                "description": obj.get("description", "")[:300],
                "tactic": obj.get("kill_chain_phases", [{}])[0].get("phase_name", "")
            })
    print(f"Loaded {len(_techniques)} MITRE techniques")

def get_relevant_techniques(incident_text: str, top_k: int = 10) -> str:
    load_mitre()
    text_lower = incident_text.lower()
    scored = []
    for t in _techniques:
        score = 0
        for word in text_lower.split():
            if len(word) > 4:
                if word in t["name"].lower() or word in t["description"].lower():
                    score += 1
        if score > 0:
            scored.append((score, t))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]
    if not top:
        top = [(0, t) for t in _techniques[:top_k]]
    return "\n".join([f"{t['id']} | {t['name']} | {t['tactic']}: {t['description']}" for _, t in top])

def _sanitize(text: str) -> str:
    """Remove asterisks from text"""
    return text.replace("*", "").replace("**", "")

def retrieve(query: str, top_k: int = 5):
    model = get_model()
    collection = get_collection()
    embedding = model.encode([query]).tolist()[0]
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    return [{"text": _sanitize(d), "source": _sanitize(m.get("name", "MITRE KB"))} for d, m in zip(docs, metas)]