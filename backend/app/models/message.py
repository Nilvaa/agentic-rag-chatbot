from datetime import datetime

from sqlalchemy import DateTime,ForeignKey,String,Column,Integer
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class Message(Base):
    __tablename__="messages"

    id=Column(Integer,primary_key=True,index=True)

    conversation_id=Column(
        Integer,
        ForeignKey("conversations.id")
    )

    role=Column(String)
    content=Column(String)
    sources=Column(JSONB,nullable=True)
    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
        )
    