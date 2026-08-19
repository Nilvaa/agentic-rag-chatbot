from sqlalchemy import ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from pgvector.sqlalchemy import Vector
from app.database import Base

class DocumentChunk(Base):
    __tablename__= "document_chunks"
    id: Mapped[int]=mapped_column(
        primary_key=True,
        index=True
    )
    document_id:Mapped[int]=mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
        index=True
    )
    content:Mapped[str]=mapped_column(
        Text,nullable=False
    )
    page_number:Mapped[int]=mapped_column(
        nullable=False
    )
    chunk_index:Mapped[int]=mapped_column(
        nullable=False
    )
    embedding:Mapped[list[float] | None]=mapped_column(
        Vector(384),
        nullable=True
    )