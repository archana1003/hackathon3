from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models
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
