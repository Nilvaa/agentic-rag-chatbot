from app.database import SessionLocal
from app.services.ingestion_service import process_document

db=SessionLocal()

try:
    chunks=process_document(
        document_id=6,
        db=db
    )
    print("Document processed successfully.")
    print("Number of chunks:", chunks)

finally:
    db.close()