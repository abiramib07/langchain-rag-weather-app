import streamlit as st
import os
from app.routes.graph import build_graph
from app.utils.pdf_loader import load_pdf
from app.embeddings.embedder import embed_documents
from app.services.weather import get_weather
from langchain_core._api.deprecation import LangChainDeprecationWarning
import warnings

# Suppress warnings
warnings.simplefilter("ignore", category=FutureWarning)
warnings.simplefilter("ignore", category=LangChainDeprecationWarning)

# Cache the document embedding
@st.cache_resource(show_spinner="Embedding and loading documents...")
def setup_app():
    pdf_path = r"E:\langchain-rag-weather-app\app\data\Virtual_Art_Exhibition_System_An_Implementation_Me.pdf"
    docs = load_pdf(pdf_path)
    embed_documents(docs)
    return build_graph()

graph = setup_app()

def run_query(query: str) -> str:
    result = graph.invoke({"input": query})
    return result['output']

# UI starts here
st.set_page_config(page_title="RAG + Weather App", layout="wide")
st.title("📄 Document Q&A + 🌤️ Weather Assistant")

query = st.text_input("Ask a question:", placeholder="e.g. What's the summary of the system OR what's the weather in Paris?")

if query:
    with st.spinner("Thinking..."):

        if "weather" in query.lower():
            response = get_weather(query)
        else:
            response = run_query(query)

        st.markdown("### 💬 Response:")
        st.write(response)
