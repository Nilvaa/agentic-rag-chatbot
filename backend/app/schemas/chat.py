from pydantic import BaseModel

class ChatRequest(BaseModel):
    question:str
    conversation_id:int | None=None

class Source(BaseModel):
    filename:str
    page:int
    chunk:int

class ChatResponse(BaseModel):
    conversation_id:int
    answer:str
    sources:list[Source] 