import os
import requests
from qdrant_client import QdrantClient
from langchain_mistralai.chat_models import ChatMistralAI
from langsmith.client import Client
from dotenv import load_dotenv

load_dotenv()

def test_env_vars():
    print("🔍 Testing environment variables...")
    required_vars = [
        "QDRANT_URL",
        "QDRANT_API_KEY",
        "MISTRAL_API_KEY",
        "OPENWEATHER_API_KEY",
        "LANGCHAIN_API_KEY",
    ]
    for var in required_vars:
        value = os.getenv(var)
        assert value, f"{var} is not set!"
    print("✅ All required environment variables are set.")

def test_openweather():
    print("🌦️ Testing OpenWeatherMap API...")
    key = os.getenv("OPENWEATHER_API_KEY")
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather",
        params={"q": "London", "appid": key}
    )
    assert response.status_code == 200, f"OpenWeatherMap failed: {response.text}"
    print("✅ OpenWeatherMap API key works.")

def test_qdrant():
    print("📦 Testing Qdrant connection...")
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    try:
        collections = client.get_collections()
        print(f"✅ Qdrant connected. Collections: {[col.name for col in collections.collections]}")
    except Exception as e:
        raise AssertionError(f"Qdrant failed: {e}")

def test_mistral():
    print("🤖 Testing Mistral LLM via LangChain...")
    try:
        llm = ChatMistralAI(model="mistral-small", api_key=os.getenv("MISTRAL_API_KEY"))
        result = llm.invoke("Say hello in one sentence")
        print(f"✅ Mistral response: {result.content}")
    except Exception as e:
        raise AssertionError(f"Mistral API failed: {e}")

def test_langsmith():
    print("🔎 Testing LangSmith connection...")
    try:
        client = Client()
        projects = list(client.list_projects())  # Convert to list
        print(f"✅ LangSmith connected. Found {len(projects)} project(s).")
    except Exception as e:
        raise AssertionError(f"LangSmith failed: {e}")


if __name__ == "__main__":
    print("🚀 Running API key & connection tests...\n")
    test_env_vars()
    test_openweather()
    test_qdrant()
    test_mistral()
    test_langsmith()
    print("\n🎉 All API and key checks passed!")
