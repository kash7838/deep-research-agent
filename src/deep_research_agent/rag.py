import os
import chromadb
from sentence_transformers import SentenceTransformer

class ResearchRAG:
    def __init__(self, persist_directory: str = "chroma_db"):
        # Initialize local persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="research_memory")
        
        # Lightweight, high-performance local embedding model
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_document(self, doc_id: str, text: str, metadata: dict = None):
        """Embed and store a research document or report chunk."""
        embedding = self.embedding_model.encode(text).tolist()
        self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {}]
        )

    def query_documents(self, query_text: str, n_results: int = 3) -> list[str]:
        """Retrieve the most relevant document chunks based on semantic similarity."""
        query_embedding = self.embedding_model.encode(query_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Extract and return the document texts
        documents = results.get("documents", [[]])
        return documents[0] if documents else []