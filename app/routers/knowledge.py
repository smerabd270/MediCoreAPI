import uuid
from fastapi import APIRouter, UploadFile, File, Depends, status
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStoreManager

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])

def get_doc_processor() -> DocumentProcessor:
    return DocumentProcessor()

def get_vector_manager() -> VectorStoreManager:
    return VectorStoreManager()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_hospital_document(
    file: UploadFile = File(...),
    processor: DocumentProcessor = Depends(get_doc_processor),
    vector_manager: VectorStoreManager = Depends(get_vector_manager)
):
    # 1. Read binary files straight from the HTTP request stream
    file_bytes = await file.read()
    
    # 2. Extract and split the text into clean data windows
    chunks = processor.process_and_chunk(file_bytes, file.filename)
    
    if not chunks:
        return {"message": f"Upload rejected. No readable text found in {file.filename}."}
        
    # 3. Save chunks into your disk-persistent vector storage database
    doc_id_prefix = f"doc_{uuid.uuid4().hex[:8]}"
    vector_manager.add_documents(chunks, doc_id_prefix)
    
    return {
        "status": "success",
        "filename": file.filename,
        "total_chunks_saved": len(chunks),
        "document_batch_id": doc_id_prefix
    }
