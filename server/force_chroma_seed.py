from app.database.database import SessionLocal
from app.models import scheme as scheme_model
from rag import embeddings
import os

def run():
    db = SessionLocal()
    schemes = db.query(scheme_model.Scheme).all()
    if not schemes:
        return
        
    print("Forcing ChromaDB generation on Render...")
    # Initialize Vector DB
    vectorstore = embeddings.get_vectorstore()
    
    # Check if already seeded to avoid rate limits on every single restart
    try:
        # ChromaDB API to get collection count
        count = len(vectorstore.get()['ids'])
        if count >= len(schemes):
            print("ChromaDB is already fully populated!")
            return
    except Exception as e:
        print("ChromaDB collection empty or failed to read, repopulating...")

    texts = []
    metadatas = []
    for s in schemes:
        full_text = f"Scheme: {s.name}\nCategory: {s.category}\nDescription: {s.description}\nEligibility: {s.eligibility}\nBenefits: {s.benefits}\nDocuments: {s.documents}"
        texts.append(full_text)
        metadatas.append({"id": s.id, "name": s.name, "category": s.category})
        
    vectorstore.add_texts(texts=texts, metadatas=metadatas)
    print("ChromaDB fully regenerated!")

if __name__ == "__main__":
    run()
