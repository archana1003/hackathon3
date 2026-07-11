import os
from sqlalchemy.orm import Session
from app.database.database import engine, Base, SessionLocal
from app.models.scheme import Scheme, Bookmark
from app.models.user import User, Profile
from rag.embeddings import get_vectorstore
from langchain_core.documents import Document

Base.metadata.create_all(bind=engine)

schemes_data = [
    {
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "category": "Agriculture",
        "description": "Income support for small/marginal farmer families.",
        "eligibility": "Must be a farmer.",
        "benefits": "6000 per year.",
        "documents": "Land records, Aadhaar, Bank account.",
        "state": "All",
        "officialLink": "https://pmkisan.gov.in/"
    },
    {
        "name": "Ayushman Bharat (PM-JAY)",
        "category": "Healthcare",
        "description": "Health insurance cover up to 5 lakh/family/year for economically vulnerable families.",
        "eligibility": "Low income families.",
        "benefits": "5 Lakh Health Insurance.",
        "documents": "Aadhaar, Ration card, Income certificate.",
        "state": "All",
        "officialLink": "https://pmjay.gov.in/"
    },
    {
        "name": "National Scholarship Portal — Post-Matric Scholarship",
        "category": "Education",
        "description": "Scholarship for students from SC/ST/OBC/minority/economically weaker backgrounds.",
        "eligibility": "Students from minority or weaker backgrounds.",
        "benefits": "Financial aid for education.",
        "documents": "Income certificate, Caste certificate, Mark sheets, Aadhaar.",
        "state": "All",
        "officialLink": "https://scholarships.gov.in/"
    },
]

db = SessionLocal()
try:
    for s_data in schemes_data:
        existing = db.query(Scheme).filter(Scheme.name == s_data["name"]).first()
        if not existing:
            scheme = Scheme(**s_data)
            db.add(scheme)
    db.commit()
    print("Database seeded with schemes.")
    
    # Try embedding into chroma
    try:
        vectorstore = get_vectorstore()
        docs = []
        for s in schemes_data:
            content = f"Scheme Name: {s['name']}\\nDescription: {s['description']}\\nEligibility: {s['eligibility']}\\nBenefits: {s['benefits']}\\nRequired Documents: {s['documents']}\\nCategory: {s['category']}\\nState: {s['state']}"
            docs.append(Document(page_content=content, metadata={"name": s['name']}))
        vectorstore.add_documents(docs)
        print("Schemes added to Vector DB (Chroma).")
    except Exception as e:
        print(f"Vector DB seeding failed (can be ignored if API key missing): {e}")

finally:
    db.close()
