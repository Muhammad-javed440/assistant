from qdrant_client import QdrantClient

# Connect to local Qdrant
client = QdrantClient(host="localhost", port=6333)

# 1. List all collections
collections = client.get_collections()
print("Collections:", collections)

# 2. Get collection info
info = client.get_collection("gemini_vectors")
print("\nCollection info:", info)

# 3. Count total points
count = client.count(collection_name="gemini_vectors", exact=True)
print("\nTotal points in gemini_vectors:", count.count)

# 4. Fetch a few points
points = client.scroll(collection_name="gemini_vectors", limit=3)
print("\nSample points:")
for point in points[0]:
    print(point)
