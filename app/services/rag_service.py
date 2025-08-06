from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain.chains import RetrievalQA
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

from app.config.settings import VECTOR_COLLECTION_NAME, QDRANT_URL, QDRANT_API_KEY

def get_rag_response(question):
    llm = ChatMistralAI(api_key=os.getenv("MISTRAL_API_KEY"))

    # ✅ Required embeddings instance
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # ✅ Client setup
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY or None,
    )

    # ✅ Pass embeddings to Qdrant
    qdrant = Qdrant(
        client=client,
        collection_name=VECTOR_COLLECTION_NAME,
        embeddings=embedding_model,
    )

    retriever = qdrant.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa.run(question)
