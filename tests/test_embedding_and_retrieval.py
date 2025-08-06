import pytest
import os
from unittest.mock import patch, MagicMock
from app.embeddings.embedder import embed_documents
# rest of imports

from unittest.mock import patch, MagicMock
from app.embeddings.embedder import embed_documents

@pytest.fixture
def sample_docs():
    # Sample minimal list of document mocks compatible with add_documents input
    return [MagicMock(content="Test doc 1"), MagicMock(content="Test doc 2")]

@patch("app.embeddings.embedder.QdrantVectorStore")
@patch("app.embeddings.embedder.HuggingFaceEmbeddings")
@patch("app.embeddings.embedder.QdrantClient")
def test_embed_documents_happy_path(
    mock_client_class, mock_embedding_class, mock_qdrant_vector_store_class, sample_docs
):
    # Setup mock for QdrantClient instance and its methods
    mock_client_instance = MagicMock()
    mock_client_instance.collection_exists.return_value = False  # simulate missing collection
    mock_client_class.return_value = mock_client_instance

    # Setup mock for HuggingFaceEmbeddings instance
    mock_embedding_instance = MagicMock()
    mock_embedding_class.return_value = mock_embedding_instance

    # Setup mock QdrantVectorStore instance
    mock_qdrant_instance = MagicMock()
    mock_qdrant_vector_store_class.return_value = mock_qdrant_instance

    # Call the actual function
    embed_documents(sample_docs)

    # Verify QdrantClient was instantiated with env variables
    mock_client_class.assert_called_once_with(
        url=None if os.getenv("QDRANT_URL") is None else os.getenv("QDRANT_URL"),
        api_key=None if os.getenv("QDRANT_API_KEY") is None else os.getenv("QDRANT_API_KEY"),
    )

    # Verify collection existence was checked
    mock_client_instance.collection_exists.assert_called_once_with("pdf_chunks")

    # Because collection did not exist, create_collection should be called once
    mock_client_instance.create_collection.assert_called_once()
    args, kwargs = mock_client_instance.create_collection.call_args
    assert kwargs["collection_name"] == "pdf_chunks"
    assert kwargs["vectors_config"].size == 384
    assert kwargs["vectors_config"].distance.name == "COSINE"

    # Verify embedding model was instantiated
    mock_embedding_class.assert_called_once_with(model_name="all-MiniLM-L6-v2")

    # Verify QdrantVectorStore constructed correctly
    mock_qdrant_vector_store_class.assert_called_once_with(
        client=mock_client_instance,
        collection_name="pdf_chunks",
        embedding=mock_embedding_instance,
    )

    # Verify add_documents was called with the provided docs
    mock_qdrant_instance.add_documents.assert_called_once_with(sample_docs)

@patch("app.embeddings.embedder.QdrantClient")
def test_embed_documents_collection_exists(mock_client_class, sample_docs):
    # Simulate collection exists
    mock_client_instance = MagicMock()
    mock_client_instance.collection_exists.return_value = True
    mock_client_class.return_value = mock_client_instance

    # Patch create_collection so it raises to detect if called erroneously
    mock_client_instance.create_collection.side_effect = Exception("Should not be called")

    with patch("app.embeddings.embedder.HuggingFaceEmbeddings") as mock_embed_class, \
         patch("app.embeddings.embedder.QdrantVectorStore") as mock_qdrant_store_class:
        
        embed_documents(sample_docs)

        # create_collection should NOT be called if collection exists
        mock_client_instance.create_collection.assert_not_called()
        # Embeddings class / vector store still constructed and add_documents called
        mock_embed_class.assert_called_once()
        mock_qdrant_store_class.assert_called_once()
