# 🌦️ RAG Weather App

A hybrid AI application that combines **Document Q&A** (RAG) with **Weather Information** using LangGraph for intelligent routing. The app automatically decides whether to fetch weather data or answer questions from uploaded PDF documents.

## 🎯 Features

- **Intelligent Routing**: LangGraph automatically routes queries to weather API or document search
- **RAG Implementation**: Query PDF documents using vector embeddings and Qdrant
- **Weather API Integration**: Real-time weather data from OpenWeatherMap
- **Streamlit UI**: Clean web interface for easy interaction
- **Vector Storage**: Qdrant cloud for document embeddings
- **AI Models**: Mistral AI for language processing

## 🏗️ Architecture

```
User Query → LangGraph Router → Decision Node
                ↓                    ↓
        Weather Keywords?     PDF Content Query?
                ↓                    ↓
         Weather Service      RAG Service
                ↓                    ↓
        OpenWeatherMap API    Qdrant Vector DB
```

## 🛠️ Technology Stack

- **Framework**: LangChain + LangGraph
- **Vector DB**: Qdrant Cloud
- **AI Models**: Mistral AI, HuggingFace Embeddings
- **Weather API**: OpenWeatherMap
- **Frontend**: Streamlit
- **Document Processing**: PyPDF

## 📋 Prerequisites

- Python 3.8+
- API Keys for:
  - Mistral AI
  - OpenWeatherMap
  - Qdrant Cloud (optional, can use local)

## 🚀 Setup Instructions

### 1. Clone & Install Dependencies

```bash
# Clone the repository
git clone <your-repo-url>
cd langchain-rag-weather-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Create Environment Variables

Create a `.env` file in the root directory:

```bash
# API Keys
MISTRAL_API_KEY=your_mistral_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Qdrant Configuration
QDRANT_URL=https://your-cluster-url.qdrant.io:6333
```

### 3. Get API Keys

#### Mistral AI API Key
1. Go to [Mistral AI Console](https://console.mistral.ai/)
2. Create account and generate API key
3. Add to `.env` file

#### OpenWeatherMap API Key
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get free API key
3. Add to `.env` file

#### Qdrant Cloud (Optional)
1. Create account at [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create cluster and get API key + URL
3. Add to `.env` file

*Or use local Qdrant: `QDRANT_URL=http://localhost:6333`*

### 4. Add Your PDF Document

Place your PDF file in:
```
app/data/your_document.pdf
```

Update the path in `main.py` and `streamlit_app.py`:
```python
pdf_path = "app/data/your_document.pdf"
```

## 🏃‍♂️ Running the Application

### Option 1: Command Line Interface
```bash
python main.py
```

### Option 2: Streamlit Web Interface
```bash
streamlit run streamlit_app.py
```

## 📝 Usage Examples

### Weather Queries
```
"What's the weather in Paris?"
"Temperature in New York today"
"Is it raining in London?"
```

### Document Queries
```
"What is the main topic of this document?"
"Summarize the key findings"
"What are the implementation details?"
```

## 🔧 Implementation Details

### LangGraph Decision Node

**Location**: `app/routes/graph.py`

```python
def route(state):
    query = state.input
    if is_weather_query(query):
        return "weather_node"
    return "rag_node"
```

The router uses keyword detection to classify queries:

**Weather Keywords**: weather, temperature, forecast, humidity, rain, sunny, cloudy, hot, cold, warm, temp, climate, precipitation, wind

### RAG Service

**Location**: `app/services/rag_service.py`

- Uses HuggingFace embeddings (`all-MiniLM-L6-v2`)
- Stores vectors in Qdrant
- Retrieval-QA chain with Mistral AI

### Weather Service

**Location**: `app/services/weather.py`

- Extracts location from natural language
- Calls OpenWeatherMap API
- Formats response with emojis

## 📁 Project Structure

```
langchain-rag-weather-app/
├── app/
│   ├── agents/
│   │   └── decision_node.py      # Weather query detection
│   ├── chains/
│   │   └── llm_chain.py          # LLM utilities
│   ├── config/
│   │   └── settings.py           # Configuration
│   ├── data/
│   │   └── your_document.pdf     # PDF documents
│   ├── embeddings/
│   │   └── embedder.py           # Document embedding
│   ├── routes/
│   │   └── graph.py              # LangGraph routing
│   ├── services/
│   │   ├── rag_service.py        # RAG implementation
│   │   └── weather.py            # Weather API service
│   └── utils/
│       └── pdf_loader.py         # PDF processing
├── main.py                       # CLI interface
├── streamlit_app.py              # Web interface
├── requirements.txt              # Dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

## 📦 Dependencies

```txt
streamlit
langchain
langchain-community
langchain-mistralai
langchain-qdrant
langgraph
qdrant-client
requests
python-dotenv
pypdf
pydantic
sentence-transformers
```

## 🔍 Troubleshooting

### Common Issues

1. **"Documents embedded in Qdrant" not showing**
   - Check Qdrant connection and API key
   - Verify collection creation permissions

2. **Weather API not working**
   - Verify OpenWeatherMap API key
   - Check network connectivity
   - Ensure location extraction is working

3. **PDF not loading**
   - Check file path is correct
   - Ensure PDF is not corrupted
   - Verify PyPDF installation

4. **Mistral AI errors**
   - Verify API key is valid
   - Check rate limits
   - Ensure sufficient credits



### Local Development
```bash
streamlit run streamlit_app.py --server.port 8501
```


## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the RAG framework
- [Qdrant](https://qdrant.tech/) for vector storage
- [Mistral AI](https://mistral.ai/) for language models
- [OpenWeatherMap](https://openweathermap.org/) for weather data
- [Streamlit](https://streamlit.io/) for the web interface

---

**Made using LangChain, LangGraph, and Streamlit**