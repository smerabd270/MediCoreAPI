import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction, OpenAIEmbeddingFunction
from app.core.config import settings

class VectorStoreManager:
    def __init__(self):
        # Spawns or connects to a persistent storage directory on your disk
        self.chroma_client = chromadb.PersistentClient(path="./vector_db")
        
        # Select the correct embedding engine based on your central configuration settings
        if getattr(settings, "AI_PROVIDER", "openai").lower() == "ollama":
            self.embedding_function = OllamaEmbeddingFunction(
                url=f"{settings.OLLAMA_BASE_URL}/api/embeddings",
                model_name=settings.OLLAMA_MODEL_NAME
            )
        else:
            self.embedding_function = OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )
            
        # Creates a unified collection for your hospital knowledge data
        self.collection = self.chroma_client.get_or_create_collection(
            name="hospital_knowledge_base",
            embedding_function=self.embedding_function
        )

    def add_documents(self, text_chunks: list[str], doc_id_prefix: str) -> None:
        """Saves textual chunks safely into the vector store database with custom indexing tags."""
        if not text_chunks:
            return
        ids = [f"{doc_id_prefix}_{i}" for i in range(len(text_chunks))]
        self.collection.add(documents=text_chunks, ids=ids)

    def query_similarity(self, query_text: str, n_results: int = 3) -> str:
        """Searches ChromaDB for semantic string context matches and outputs a combined text result."""
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        if results and results.get("documents") and results["documents"]:
            # Flatten retrieved array entries into a single paragraph for prompt injection
            return "\n\n".join(results["documents"][0])
        return ""
