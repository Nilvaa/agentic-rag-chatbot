from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.database import engine,Base
from app.models.document import Document
from app.schemas.document import DocumentCreate
from app.routers.documents import router as documents_router
from app.routers.chat import router as chat_router
from app.routers.conversation import router as conversation_router
from app.routers.auth import router as auth_router

app=FastAPI(
    title="Agentic RAG API",
    version="1.0.0"
)

app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(conversation_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return {"message":"Agentic RAG API is running"}

@app.get("/health")
def health_check(db:Session=Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status":"healthy",
        "database":"connected"
    }

@app.post("/documents")
def create_document(
    document:DocumentCreate,
    db: Session = Depends(get_db)
):
    new_document=Document(
        filename=document.filename
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document

@app.get("/documents")
def get_documents(db:Session=Depends(get_db)):
    documents=db.query(Document).all()
    return documents

@app.get("/documents/{document_id}")
def get_document(
    document_id:int,
    db: Session=Depends(get_db)
):
    document=db.query(Document).filter(
        Document.id==document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    return document

@app.delete("/documents/{document_id}")
def delete_document(
    document_id:int,
    db: Session=Depends(get_db)
):
    document=db.query(Document).filter(
        Document.id==document_id
    ).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    db.delete(document)
    db.commit()

    return {
        "message":"Document deleted successfully"
    }