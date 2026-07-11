import os
import pandas as pd
from app.database.database import SessionLocal, engine
from app.models import scheme as scheme_model
from rag import embeddings

# Setup DB
scheme_model.Base.metadata.create_all(bind=engine)

def seed_from_csv():
    # 1. Load CSV
    csv_path = '../updated_data.csv'
    df = pd.read_csv(csv_path)
    
    # Take first 20 rows to avoid API rate limits during the hackathon
    sample_df = df.head(20)

    # 2. Database Session
    db = SessionLocal()
    
    # 3. Vector DB
    vectorstore = embeddings.get_vectorstore()

    texts_to_embed = []
    metadatas = []

    print("Seeding database with schemes from CSV...")

    for index, row in sample_df.iterrows():
        # Map CSV columns to our schema
        name = str(row.get('scheme_name', 'Unknown Scheme'))
        category = str(row.get('schemeCategory', 'General'))
        description = str(row.get('details', 'No description provided.'))
        eligibility = str(row.get('eligibility', 'Check official guidelines.'))
        benefits = str(row.get('benefits', 'Various benefits.'))
        documents = str(row.get('documents', 'Standard KYC documents.'))

        # Check if already exists in DB
        existing = db.query(scheme_model.Scheme).filter(scheme_model.Scheme.name == name).first()
        if not existing:
            new_scheme = scheme_model.Scheme(
                name=name,
                category=category,
                description=description,
                eligibility=eligibility,
                benefits=benefits,
                documents=documents,
                officialLink="" # Not strongly defined in CSV
            )
            db.add(new_scheme)
            db.commit()
            db.refresh(new_scheme)
            
            # Prepare for Vector DB
            full_text = f"Scheme: {name}\nCategory: {category}\nDescription: {description}\nEligibility: {eligibility}\nBenefits: {benefits}\nDocuments: {documents}"
            texts_to_embed.append(full_text)
            metadatas.append({"id": new_scheme.id, "name": name, "category": category})
            print(f"Added: {name}")

    db.close()

    if texts_to_embed:
        print("Adding to Vector DB (Chroma)... This might take a few seconds.")
        vectorstore.add_texts(texts=texts_to_embed, metadatas=metadatas)
        print("Vector DB updated successfully!")
    else:
        print("No new schemes to add.")

if __name__ == "__main__":
    seed_from_csv()
