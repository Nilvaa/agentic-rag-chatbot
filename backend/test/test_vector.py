from app.database import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.models.document import Document
from app.services.vector_service import VectorService

db=SessionLocal()
try:
    chunk=(
        db.query(DocumentChunk).filter(DocumentChunk.embedding.is_(None)).first()
    )

    if not chunk:
        print("No unembedded chunks found.")
    else:
        print("Processing Chunk:",chunk.id)
        service=VectorService()
        service.embed_chunk(
            chunk=chunk,db=db
        )
        print("Embedding stored successfully.")
        print("Embedding dimensions:", len(chunk.embedding))
finally:
    db.close()