from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_pages

def process_document(
        document_id:int,
        db:Session
):
    document=db.get(Document,document_id)

    if not document:
        raise ValueError("Document not found")

    try:
        document.status="PROCESSING"
        db.commit()

        pages=extract_text_from_pdf(
            document.file_path
        )
        chunks=chunk_pages(pages)

        for chunk in chunks:
            document_chunk=DocumentChunk(
                document_id=document.id,
                content=chunk["content"],
                page_number=chunk["page_number"],
                chunk_index=chunk["chunk_index"]
            )
            db.add(document_chunk)

        document.status="COMPLETED"
        db.commit()
        return len(chunks)
    except Exception:
        document.status="FAILED"
        db.commit()
        raise
