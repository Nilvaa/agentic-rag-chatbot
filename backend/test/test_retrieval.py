from app.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.retrieval_service import RetrievalService

db=SessionLocal()

try:
    service=RetrievalService()
    query="What does Apple say about human rights?"
    results=service.search(query=query,db=db,top_k=3)
    print("\nSearch results:")
    print("=" * 60)

    
    for chunk, distance in results:
        print(f"Document ID : {chunk.document_id}")
        print(f"Page        : {chunk.page_number}")
        print(f"Chunk       : {chunk.chunk_index}")
        print(f"Distance    : {distance:.4f}")
        print(f"Content     : {chunk.content[:300]}")
        print("=" * 60)

finally:
    db.close()