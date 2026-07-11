from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    occupation: Optional[str] = None
    income: Optional[int] = None
    category: Optional[str] = None
    farmer: Optional[bool] = False
    student: Optional[bool] = False
    disabled: Optional[bool] = False
    widow: Optional[bool] = False
    seniorCitizen: Optional[bool] = False
