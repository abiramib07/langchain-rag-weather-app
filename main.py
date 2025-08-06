from app.routes.graph import build_graph

from app.utils.pdf_loader import load_pdf
from app.embeddings.embedder import embed_documents
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import warnings

from langchain_core._api.deprecation import LangChainDeprecationWarning

# Suppress LangChain-specific deprecation warnings
warnings.simplefilter("ignore", category=LangChainDeprecationWarning)

# Also suppress future warnings if you haven't already
warnings.simplefilter("ignore", category=FutureWarning)

docs = load_pdf(r"E:\langchain-rag-weather-app\app\data\Virtual_Art_Exhibition_System_An_Implementation_Me.pdf")

embed_documents(docs)
print("Documents embedded in Qdrant.")

def run_query(query):
    graph = build_graph()
    result = graph.invoke({"input": query})
    return result['output']

if __name__ == "__main__":
    while True:
        q = input("Ask something: ")
        print(run_query(q))
