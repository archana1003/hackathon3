from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    
    profile = relationship("Profile", back_populates="user", uselist=False)
    bookmarks = relationship("Bookmark", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"))
    age = Column(Integer)
    gender = Column(String)
    state = Column(String)
    district = Column(String)
    occupation = Column(String)
    income = Column(Integer)
    category = Column(String)
    farmer = Column(Boolean, default=False)
    student = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    widow = Column(Boolean, default=False)
    seniorCitizen = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="profile")
