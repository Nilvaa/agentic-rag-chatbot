from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import EmbeddingService

class VectorService:
    def __init__(self):
        self.embedding_service=EmbeddingService()

    def embed_chunk(self,chunk:DocumentChunk,db:Session):
        embedding=self.embedding_service.generate_embedding(
            chunk.content
        )
        chunk.embedding=embedding

        db.commit()
        db.refresh(chunk)

        return chunk

    def embed_pending_chunk(self,db:Session):
        chunks=(db.query(DocumentChunk).filter(DocumentChunk.embedding.is_(None)).all())

        if not chunks:
            return 0
        texts=[chunk.content for chunk in chunks]

        embeddings=self.embedding_service.model.encode(texts,normalize_embeddings=True)

        for chunk,embedding in zip(chunks,embeddings):
            chunk.embedding=embedding.tolist()
        db.commit()
        return len(chunks)
