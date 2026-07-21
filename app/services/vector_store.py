import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction, OpenAIEmbeddingFunction
from app.core.config import settings

class VectorStoreManager:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="./vector_db")
        
        if getattr(settings, "AI_PROVIDER", "openai").lower() == "ollama":
            # FIX: ChromaDB natively appends endpoint routes. Provide ONLY the base host URL.
            self.embedding_function = OllamaEmbeddingFunction(
                url=settings.OLLAMA_BASE_URL,
                model_name=settings.OLLAMA_MODEL_NAME
            )
        else:
            self.embedding_function = OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )
            
        self.collection = self.chroma_client.get_or_create_collection(
            name="hospital_knowledge_base",
            embedding_function=self.embedding_function
        )

    def add_documents(self, text_chunks: list[str], doc_id_prefix: str) -> None:
        if not text_chunks:
            return
        ids = [f"{doc_id_prefix}_{i}" for i in range(len(text_chunks))]
        self.collection.add(documents=text_chunks, ids=ids)

    def query_similarity(self, query_text: str, n_results: int = 3) -> str:
        results = self.collection.query(query_texts=[query_text], n_results=n_results)
        if results and results.get("documents") and results["documents"]:
            return "\n\n".join(results["documents"])
        return ""
