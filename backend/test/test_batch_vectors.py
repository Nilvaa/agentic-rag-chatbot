from app.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.vector_service import VectorService

db=SessionLocal()
try:
    service=VectorService()
    count= service.embed_pending_chunk(db)
    print("Embeddings generated:", count)
finally:
    db.close()