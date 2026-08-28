from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.chat import ChatRequest,ChatResponse
from app.services.agent_service import AgentService
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User

from app.dependencies.auth import get_current_user

router=APIRouter(
    prefix="/chat",
    tags=["Chats"]
)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

def generate_title(question:str):
    title=question.strip()

    if len(title)>50:
        title=title[:50].rstrip()+"..."
    return title

@router.post("/",response_model=ChatResponse)
def chat(
    request:ChatRequest,
    db:Session=Depends(get_db),
    current_user: User=Depends(get_current_user)
):

    #to get existing conversation id / create new 
    if request.conversation_id is not None:
        conversation=db.query(Conversation).filter(
            Conversation.id==request.conversation_id,
            Conversation.user_id==current_user.id
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
    else:
        conversation=Conversation(
            user_id=current_user.id,
            title=generate_title(request.question)
        )
        db.add(conversation)
        db.flush()

    #save user question
    user_message=Message(
                conversation_id=conversation.id,
                role="user",
                content=request.question
            )    
        
    db.add(user_message)
    db.flush()


    #to get previous conversation messages
    previous_messages=(
        db.query(Message)
        .filter(Message.conversation_id==conversation.id,
                Message.id!=user_message.id
            ).order_by(Message.created_at)
            .all()
    )

    history="\n".join(
        f"{message.role}:{message.content}"
        for message in previous_messages
    )

        
    agent=AgentService()

    result=agent.run(
        question=request.question,
        db=db,
        history=history
    )

    answer=result["answer"]
    sources=result["sources"]

    assistant_message=Message(
        conversation_id=conversation.id,
        role="assistant",
        content=answer,
        sources=sources
    )

    db.add(assistant_message)
    db.commit()

    return {
        "conversation_id":conversation.id,
        "answer":answer,
        "sources":sources
    }
