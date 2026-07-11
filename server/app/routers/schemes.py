from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.scheme import SchemeOut, BookmarkCreate
from app.models.scheme import Scheme, Bookmark
from app.models.user import User, Profile
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api")

@router.get("/schemes", response_model=List[SchemeOut])
def get_schemes(db: Session = Depends(get_db)):
    return db.query(Scheme).all()

@router.get("/schemes/{scheme_id}", response_model=SchemeOut)
def get_scheme(scheme_id: int, db: Session = Depends(get_db)):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme

@router.post("/recommend", response_model=List[SchemeOut])
def recommend_schemes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.userId == current_user.id).first()
    if not profile:
        return []
    
    # Basic matching logic (in reality, this would be an AI engine or complex rules)
    schemes = db.query(Scheme).all()
    recommended = []
    for s in schemes:
        # Example rule: if state matches or is 'All'
        state = s.state or 'all'
        if state.lower() == 'all' or (profile.state and profile.state.lower() in state.lower()):
            recommended.append(s)
            
    return recommended

@router.post("/bookmark")
def create_bookmark(bookmark: BookmarkCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Bookmark).filter(Bookmark.userId == current_user.id, Bookmark.schemeId == bookmark.schemeId).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already bookmarked")
    new_bm = Bookmark(userId=current_user.id, schemeId=bookmark.schemeId)
    db.add(new_bm)
    db.commit()
    return {"message": "Bookmark created"}

@router.get("/bookmarks", response_model=List[SchemeOut])
def get_bookmarks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bookmarks = db.query(Bookmark).filter(Bookmark.userId == current_user.id).all()
    scheme_ids = [bm.schemeId for bm in bookmarks]
    if not scheme_ids:
        return []
    schemes = db.query(Scheme).filter(Scheme.id.in_(scheme_ids)).all()
    return schemes

@router.get("/search", response_model=List[SchemeOut])
def search_schemes(q: str = "", category: str = "", state: str = "", db: Session = Depends(get_db)):
    query = db.query(Scheme)
    if q:
        query = query.filter(Scheme.name.ilike(f"%{q}%"))
    if category:
        query = query.filter(Scheme.category.ilike(f"%{category}%"))
    if state:
        query = query.filter(Scheme.state.ilike(f"%{state}%"))
    return query.all()
