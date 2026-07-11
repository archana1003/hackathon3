from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database.database import Base
import datetime

class Scheme(Base):
    __tablename__ = "schemes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    eligibility = Column(Text)
    benefits = Column(Text)
    documents = Column(Text)
    state = Column(String)
    category = Column(String)
    officialLink = Column(String)

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"))
    schemeId = Column(Integer, ForeignKey("schemes.id"))
    
    user = relationship("User", back_populates="bookmarks")
    scheme = relationship("Scheme")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"))
    question = Column(Text)
    answer = Column(Text)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="chat_history")
