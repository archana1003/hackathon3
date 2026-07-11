import os

# schemas/scheme.py
with open("app/schemas/scheme.py", "w") as f:
    f.write("""from pydantic import BaseModel
from typing import Optional, List

class SchemeBase(BaseModel):
    name: str
    description: str
    eligibility: str
    benefits: str
    documents: str
    state: str
    category: str
    officialLink: str

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
""")

# routers/schemes.py
with open("app/routers/schemes.py", "w") as f:
    f.write("""from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.scheme import SchemeOut, BookmarkCreate
from app.models.scheme import Scheme, Bookmark
from app.models.user import User, Profile
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api")

@router.get("/schemes", response_model=List[SchemeOut])
def get_schemes(db: Session = Depends(get_db)):
    return db.query(Scheme).all()

@router.get("/schemes/{scheme_id}", response_model=SchemeOut)
def get_scheme(scheme_id: int, db: Session = Depends(get_db)):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme

@router.post("/recommend", response_model=List[SchemeOut])
def recommend_schemes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.userId == current_user.id).first()
    if not profile:
        return []
    
    # Basic matching logic (in reality, this would be an AI engine or complex rules)
    schemes = db.query(Scheme).all()
    recommended = []
    for s in schemes:
        # Example rule: if state matches or is 'All'
        if s.state.lower() == 'all' or (profile.state and profile.state.lower() in s.state.lower()):
            recommended.append(s)
            
    return recommended

@router.post("/bookmark")
def create_bookmark(bookmark: BookmarkCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Bookmark).filter(Bookmark.userId == current_user.id, Bookmark.schemeId == bookmark.schemeId).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already bookmarked")
    new_bm = Bookmark(userId=current_user.id, schemeId=bookmark.schemeId)
    db.add(new_bm)
    db.commit()
    return {"message": "Bookmark created"}

@router.get("/bookmarks", response_model=List[SchemeOut])
def get_bookmarks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bookmarks = db.query(Bookmark).filter(Bookmark.userId == current_user.id).all()
    scheme_ids = [bm.schemeId for bm in bookmarks]
    if not scheme_ids:
        return []
    schemes = db.query(Scheme).filter(Scheme.id.in_(scheme_ids)).all()
    return schemes

@router.get("/search", response_model=List[SchemeOut])
def search_schemes(q: str = "", category: str = "", state: str = "", db: Session = Depends(get_db)):
    query = db.query(Scheme)
    if q:
        query = query.filter(Scheme.name.ilike(f"%{q}%"))
    if category:
        query = query.filter(Scheme.category.ilike(f"%{category}%"))
    if state:
        query = query.filter(Scheme.state.ilike(f"%{state}%"))
    return query.all()
""")

# routers/chatbot.py
with open("app/routers/chatbot.py", "w") as f:
    f.write("""from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.scheme import ChatRequest, ChatResponse
from app.models.user import User
from app.models.scheme import ChatHistory
from app.services.auth_service import get_current_user
from langchain_core.messages import HumanMessage, SystemMessage
from rag.embeddings import get_llm, get_vectorstore

router = APIRouter(prefix="/api")

@router.post("/chat", response_model=ChatResponse)
def chat_with_bot(chat: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    llm = get_llm()
    vectorstore = get_vectorstore()
    
    # Retrieve docs
    try:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(chat.question)
        context = "\\n".join([d.page_content for d in docs])
    except Exception as e:
        context = "No additional context found."
        
    system_prompt = \"\"\"You are JanSeva AI, an assistant helping Indian citizens with government schemes.
Answer the user's question based ONLY on the provided context. If unsure, say "I could not find this information in the government database." Do not invent schemes or provide legal advice.

Context:
{context}\"\"\"

    messages = [
        SystemMessage(content=system_prompt.format(context=context)),
        HumanMessage(content=chat.question)
    ]
    
    response = llm.invoke(messages)
    answer = response.content
    
    # Save chat history
    history = ChatHistory(userId=current_user.id, question=chat.question, answer=answer)
    db.add(history)
    db.commit()
    
    return {"answer": answer}
""")

# Update main.py
with open("app/main.py", "w") as f:
    f.write("""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routers import auth, schemes, chatbot

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="JanSeva AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(schemes.router)
app.include_router(chatbot.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to JanSeva AI API"}
""")
