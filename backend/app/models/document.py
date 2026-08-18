from datetime import datetime
from sqlalchemy import DateTime,String
from sqlalchemy.orm import Mapped,mapped_column

from app.database import Base

class Document(Base):
    __tablename__= "documents"

    id: Mapped[int]=mapped_column(
        primary_key=True,
        index=True
    )

    filename: Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )

    file_path: Mapped[str]=mapped_column(
        String(500),
        nullable=False
    )

    file_type: Mapped[str]=mapped_column(
        String(50),
        nullable=False
    )

    file_size: Mapped[int]=mapped_column(
        nullable=False
    )

    status: Mapped[str]=mapped_column(
        String(20),
        default="PENDING",
        nullable=False
    )

    created_at: Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )