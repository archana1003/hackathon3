import sys
import sqlite3
if sqlite3.sqlite_version_info < (3, 35, 0):
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.models
from app.database.database import engine, Base
from app.routers import auth, schemes, chatbot

# Create DB tables
Base.metadata.create_all(bind=engine)

# Force Vector DB generation if empty
try:
    import force_chroma_seed
    force_chroma_seed.run()
except Exception as e:
    print("Warning: Chroma seed failed:", e)

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
