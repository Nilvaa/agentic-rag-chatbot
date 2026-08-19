from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import EmbeddingService

class RetrievalService:
    def __init__(self):
        self.embedding_service=EmbeddingService()

    def search(
            self,query:str,db:Session,top_k:int=3
    ):
        query_embedding=(
            self.embedding_service.generate_embedding(query)
        )

        results=(
            db.query(DocumentChunk,DocumentChunk.embedding.cosine_distance(query_embedding).label("distance"))
            .filter(DocumentChunk.embedding.is_not(None))
            .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
            .limit(top_k).all()
        )
        return results