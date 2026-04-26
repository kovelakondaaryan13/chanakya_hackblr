from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import math, hashlib
from data import DOCUMENTS, QDRANT_URL, QDRANT_API_KEY

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
COLLECTION = "chanakya"
DIM = 384

def simple_embed(text):
    h = hashlib.sha256(text.encode()).digest()
    vec = [math.sin((h[i % 32] + i) * 0.1) for i in range(DIM)]
    norm = sum(x**2 for x in vec) ** 0.5
    return [x / norm for x in vec]

def setup():
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION in existing:
        client.delete_collection(COLLECTION)
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=DIM, distance=Distance.COSINE)
    )
    points = [
        PointStruct(id=i, vector=simple_embed(doc), payload={"text": doc})
        for i, doc in enumerate(DOCUMENTS)
    ]
    client.upsert(collection_name=COLLECTION, points=points)
    print(f"Loaded {len(points)} documents into Qdrant")

if __name__ == "__main__":
    setup()
