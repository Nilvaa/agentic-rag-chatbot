from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.dependencies.auth import get_current_user

router=APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_conversations(
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    conversations=(
        db.query(Conversation)
        .filter(Conversation.user_id==current_user.id)
        .order_by(Conversation.created_at.desc())
        .all()
    )

    return conversations

@router.get("/{conversation_id}")
def get_conversation(
    conversation_id:int,
    db:Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    conversation=(
        db.query(Conversation)
        .filter(Conversation.id==conversation_id,
                Conversation.user_id==current_user.id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="conversation not found"
        )

    messages=(
        db.query(Message)
        .filter(Message.conversation_id==conversation_id)
        .order_by(Message.created_at)
        .all()
    )

    return {
        "id":conversation.id,
        "created_at":conversation.created_at,
        "updated_at":conversation.updated_at,
        "messages":[
            {
                "id":message.id,
                "role":message.role,
                "content":message.content,
                "created_at":message.created_at
            }
            for message in messages
        ]
    }

@router.delete("/{conversation_id}")
def delete_conversations(
    conversation_id:int,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):
    conversation=(
        db.query(Conversation)
        .filter(Conversation.id==conversation_id,
                Conversation.user_id==current_user.id)
        .first()
        )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="conversation not found"
        )

    #delete messages first
    db.query(Message).filter(
        Message.conversation_id==conversation_id
    ).delete()

    db.delete(conversation)

    db.commit()

    return {
        "message":"conversation deleted successfully",
        "conversation_id":conversation_id
    }