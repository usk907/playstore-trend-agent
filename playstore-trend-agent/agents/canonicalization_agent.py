import json
import numpy as np
import hashlib
import os
from sklearn.metrics.pairwise import cosine_similarity

SIM_THRESHOLD = 0.85
MEMORY_FILE = "storage/topic_memory.json"

os.makedirs("storage", exist_ok=True)

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def embed(text):
    h = hashlib.sha256(text.encode()).digest()
    np.random.seed(int.from_bytes(h[:4], "little"))
    return np.random.rand(384).tolist()

def canonicalize(topic):
    memory = load_memory()
    topic_emb = embed(topic)

    for entry in memory:
        sim = cosine_similarity(
            [topic_emb], [entry["embedding"]]
        )[0][0]
        if sim >= SIM_THRESHOLD:
            return entry["canonical_name"]

    new_entry = {
        "canonical_name": topic,
        "embedding": topic_emb
    }
    memory.append(new_entry)
    save_memory(memory)
    return topic
