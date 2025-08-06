from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import os
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

def embed_documents(docs):
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

    # Make sure the collection exists
    collection_name = "pdf_chunks"
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # size must match embedding dim
        )

    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    qdrant = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding,
    )

    qdrant.add_documents(docs)
