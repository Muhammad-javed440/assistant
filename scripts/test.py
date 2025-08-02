from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue

# Step 1: Initialize in-memory Qdrant client
client = QdrantClient(":memory:")
print("✅ Qdrant client initialized.")

# Step 2: Define collection
collection_name = "my_collection"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=4, distance=Distance.COSINE),
)
print(f"✅ Collection '{collection_name}' created.")

# Step 3: Upload some sample vectors
vectors = [
    [0.1, 0.2, 0.3, 0.4],
    [0.5, 0.6, 0.7, 0.8],
    [0.9, 0.1, 0.3, 0.7],
]
ids = [1, 2, 3]

client.upsert(
    collection_name=collection_name,
    points=[
        PointStruct(id=ids[i], vector=vectors[i]) for i in range(len(vectors))
    ]
)
print("✅ Vectors uploaded.")

# Step 4: Perform a vector similarity search
search_result = client.search(
    collection_name=collection_name,
    query_vector=[0.1, 0.2, 0.3, 0.4],
    limit=2,
)

print("\n🔍 Search results:")
for result in search_result:
    print(f"ID: {result.id}, Score: {result.score:.4f}")
