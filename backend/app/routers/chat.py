from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from datetime import datetime,timezone

from app.database import SessionLocal
from app.schemas.chat import ChatRequest,ChatResponse
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.models.conversation import Conversation
from app.models.message import Message

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

@router.post("/",response_model=ChatResponse)
def chat(
    request:ChatRequest,
    db:Session=Depends(get_db)
):

    #to get existing conversation id / create new 
    if request.conversation_id:
        conversation=db.query(Conversation).filter(
            Conversation.id==request.conversation_id
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
    else:
        conversation=Conversation()
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
            ).order_by(Message.id)
            .all()
    )

    history="\n".join(
        f"{message.role}:{message.content}"
        for message in previous_messages
    )

        
    retrieve_service=RetrievalService()

    results=retrieve_service.search(
        query=request.question,
        db=db,
        top_k=3
    )

    context = "\n\n".join(
        f"""
Source: {filename}
Page: {chunk.page_number}
Chunk: {chunk.chunk_index}

{chunk.content}
"""
        for chunk, filename, distance in results
    )

    llm_service=LLMService()

    answer=llm_service.generate_answer(
        question=request.question,
        context=context,
        history=history
    )

    assistant_message=Message(
        conversation_id=conversation.id,
        role="assistant",
        content=answer
    )

    db.add(assistant_message)
    conversation.updated_at=datetime.now(timezone.utc)
    db.commit()


    sources=[
        {
            "filename":filename,
            "page":chunk.page_number,
            "chunk":chunk.chunk_index
        }
        for chunk,filename,distance in results
    ]

    return {
        "conversation_id":conversation.id,
        "answer":answer,
        "sources":sources
    }
