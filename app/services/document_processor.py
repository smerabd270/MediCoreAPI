import io
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def extract_text_from_bytes(self, file_bytes: bytes, filename: str) -> str:
        if filename.lower().endswith(".pdf"):
            pdf_stream = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_stream)
            extracted_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
            return "\n".join(extracted_text)
        return file_bytes.decode("utf-8", errors="ignore")

    def process_and_chunk(self, file_bytes: bytes, filename: str) -> list[str]:
        raw_text = self.extract_text_from_bytes(file_bytes, filename)
        if not raw_text.strip():
            return []
        return self.text_splitter.split_text(raw_text)
