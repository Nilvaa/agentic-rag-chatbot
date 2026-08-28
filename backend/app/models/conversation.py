from sqlalchemy import DateTime,Column,Integer,ForeignKey,String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Conversation(Base):
    __tablename__="conversations"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id=Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title=Column(
        String,
        nullable=False
    )
    created_at=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at=Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user=relationship(
        "User",
        back_populates="conversations"
    )