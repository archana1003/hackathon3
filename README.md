# JanSeva AI

JanSeva AI is an AI-powered government scheme eligibility & guidance assistant. It helps Indian citizens discover government welfare schemes they are likely eligible for by collecting only basic demographic and socioeconomic information.

## Tech Stack
- **Frontend:** React 19, Vite, Tailwind CSS, React Router DOM, Axios, Context API, Framer Motion
- **Backend:** FastAPI, PostgreSQL (SQLite for local dev fallback), SQLAlchemy, JWT Auth
- **AI:** Gemini / LangChain / ChromaDB for RAG-based Chatbot

## Setup Instructions

### 1. Backend Setup
```bash
cd server
python -m venv venv
# Activate virtualenv (Windows: .\venv\Scripts\activate, Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
```
Copy `.env.example` to `.env` and fill in your keys:
```env
DATABASE_URL=sqlite:///./janseva.db
JWT_SECRET=supersecretkey
GEMINI_API_KEY=your_gemini_api_key
```

Seed the database and vector DB:
```bash
python seed_schemes.py
```

Run the server:
```bash
uvicorn app.main:app --reload
```
Server runs on http://localhost:8000.

### 2. Frontend Setup
```bash
cd client
npm install
npm run dev
```
Frontend runs on http://localhost:5173.

## Features
- **Smart Eligibility Match:** Enter basic details to instantly see schemes you qualify for.
- **AI Chatbot Assistant:** Ask any questions and get answers from verified government data.
- **Multilingual Ready:** Architecture prepared for adding multi-language support.
- **Bookmarking:** Save schemes to your profile.
- **Secure:** JWT Auth, hashed passwords, no sensitive documents stored.
