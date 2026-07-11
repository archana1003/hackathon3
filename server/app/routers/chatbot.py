from fastapi import APIRouter, Depends
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
        context = "\n".join([d.page_content for d in docs])
    except Exception as e:
        context = "No additional context found."
        
    system_prompt = """You are JanSeva AI, an assistant helping Indian citizens with government schemes.
Answer the user's question based ONLY on the provided context. If unsure, say "I could not find this information in the government database." Do not invent schemes or provide legal advice.

Context:
{context}"""

    messages = [
        SystemMessage(content=system_prompt.format(context=context)),
        HumanMessage(content=chat.question)
    ]
    
    response = llm.invoke(messages)
    answer = response.content
    
    # Langchain might return a list of text blocks for some models
    if isinstance(answer, list):
        answer = answer[0].get("text", str(answer)) if isinstance(answer[0], dict) else str(answer)
        
    # Save chat history
    history = ChatHistory(userId=current_user.id, question=chat.question, answer=answer)
    db.add(history)
    db.commit()
    
    return {"answer": answer}
