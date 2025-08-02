# #!/usr/bin/env python3
# """
# Add Gemini Embeddings to Qdrant
# ==============================

# This script reads Gemini embeddings from a JSON file and inserts them into a Qdrant collection.

# Usage:
#     python add_gemini_embeddings_to_qdrant.py

# Requirements:
#     - pip install qdrant-client
#     - Qdrant running locally (see vectordb/README.md)
# """
# import json
# from pathlib import Path

# from qdrant_client import QdrantClient 
# from qdrant_client.models import Distance, PointStruct, VectorParams  

# # Config
# EMBEDDINGS_PATH = Path("data/rag_ready/rag_ready_data.json")
# COLLECTION_NAME = "gemini_vectors"
# VECTOR_SIZE = 1536  # Default for gemini-embedding-001
# QDRANT_HOST = "localhost"
# QDRANT_PORT = 6333
# QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.GRpaIddEvjeH-WUUwXXm0rdyhpwiuhkJFGZi1Zd6zZM"

# # Load embeddings
# with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
#     data = json.load(f)
#     embeddings = data.get("embeddings", [])

# if not embeddings:
#     raise ValueError(f"No embeddings found in {EMBEDDINGS_PATH}")

# # Connect to Qdrant
# client = QdrantClient(QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)

# # Create collection if not exists
# client.recreate_collection(
#     collection_name=COLLECTION_NAME,
#     vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
# )

# # Prepare points
# points = []
# for idx, item in enumerate(embeddings):
#     vector = item["embedding"]
#     payload = {
#         "id": item.get("id"),
#         "content": item.get("content"),
#         "content_type": item.get("content_type"),
#         "source_url": item.get("source_url"),
#         "metadata": item.get("metadata", {}),
#     }
#     points.append(PointStruct(id=idx, vector=vector, payload=payload))

# # Insert into Qdrant
# client.upsert(collection_name=COLLECTION_NAME, points=points)
# print(
#     f"Inserted {len(points)} Gemini embeddings into Qdrant collection '{COLLECTION_NAME}'"
# )





#!/usr/bin/env python3
"""
Add Gemini Embeddings to Qdrant
===============================

This script reads content chunks from a JSON file, generates Gemini embeddings,
and inserts them into a Qdrant collection.

Usage:
    uv run scripts/sample.py

Requirements:
    - Qdrant running locally (e.g., via Docker)
    - pip install qdrant-client
"""

import json
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

# === CONFIG ===
EMBEDDINGS_PATH = Path("data/rag_ready/rag_ready_data.json")
COLLECTION_NAME = "gemini_vectors"
VECTOR_SIZE = 1536  # Typical size for Gemini/embedding models
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_API_KEY = None  # Not needed for local Qdrant

# === STUB: Replace this with real Gemini API ===
def generate_embedding(text: str) -> list[float]:
    # TODO: Replace this stub with a real embedding generator
    return [0.0] * VECTOR_SIZE  # Dummy vector for testing

# === LOAD CHUNKS ===
with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
    raw_chunks = json.load(f)

# === GENERATE EMBEDDINGS ===
embeddings = []
for item in raw_chunks:
    content = item.get("content", "")
    if not content.strip():
        continue

    vector = generate_embedding(content)

    embeddings.append({
        "id": item.get("id"),
        "embedding": vector,
        "content": content,
        "metadata": item.get("metadata", {}),
        "content_type": item.get("content_type", "text"),
        "source_url": item.get("metadata", {}).get("original_url", None),
    })

if not embeddings:
    raise ValueError(f"No embeddings generated from {EMBEDDINGS_PATH}")

# === CONNECT TO QDRANT ===
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)

# === (RE)CREATE COLLECTION ===
if client.collection_exists(collection_name=COLLECTION_NAME):
    client.delete_collection(collection_name=COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
)

# === INSERT INTO QDRANT ===
points = []
for idx, item in enumerate(embeddings):
    points.append(
        PointStruct(
            id=idx,
            vector=item["embedding"],
            payload={
                "id": item["id"],
                "content": item["content"],
                "metadata": item["metadata"],
                "content_type": item["content_type"],
                "source_url": item["source_url"],
            },
        )
    )

client.upsert(collection_name=COLLECTION_NAME, points=points)
print(f"✅ Inserted {len(points)} embeddings into Qdrant collection '{COLLECTION_NAME}'")
