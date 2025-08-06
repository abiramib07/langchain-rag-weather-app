from unittest.mock import patch, MagicMock
from qdrant_client import QdrantClient
from app.services.rag_service import get_rag_response

@patch("app.services.rag_service.RetrievalQA.from_chain_type")
@patch("app.services.rag_service.ChatMistralAI")
def test_get_rag_response_success(mock_chat_mistralai, mock_retrieval_qa):
    mock_qa_instance = MagicMock()
    mock_qa_instance.run.return_value = "This is a mock RAG response"
    mock_retrieval_qa.return_value = mock_qa_instance

    mock_chat_mistralai.return_value = MagicMock()

    # Create a real QdrantClient instance with dummy params
    dummy_client = QdrantClient(url="http://localhost:6333", api_key="dummy_api_key")

    with patch("app.services.rag_service.QdrantClient", return_value=dummy_client):
        question = "Tell me about the virtual exhibition system."
        response = get_rag_response(question)

    assert response == "This is a mock RAG response"
    mock_retrieval_qa.assert_called_once()
    mock_qa_instance.run.assert_called_once_with(question)
