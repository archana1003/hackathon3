from pydantic import BaseModel
from typing import Optional, List

class SchemeBase(BaseModel):
    name: str
    description: str
    eligibility: str
    benefits: str
    documents: str
    state: Optional[str] = None
    category: str
    officialLink: Optional[str] = None

class SchemeOut(SchemeBase):
    id: int

    class Config:
        orm_mode = True

class BookmarkCreate(BaseModel):
    schemeId: int

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
