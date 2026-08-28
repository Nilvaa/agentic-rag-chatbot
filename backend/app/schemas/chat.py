from pydantic import BaseModel

class ChatRequest(BaseModel):
    question:str
    conversation_id:int | None=None

class Source(BaseModel):
    type:str
    filename:str | None=None
    page:int | None=None
    chunk:int |None=None

    title:str | None=None
    url:str | None=None

class ChatResponse(BaseModel):
    conversation_id:int
    answer:str
    sources:list[Source] 