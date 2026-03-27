from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.bookmark import Bookmark
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])

# TOGGLE BOOKMARK
@router.post("/{post_id}")
def bookmark_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.post_id == post_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"message": "Removed bookmark"}

    new_bookmark = Bookmark(user_id=current_user.id, post_id=post_id)
    db.add(new_bookmark)
    db.commit()

    return {"message": "Bookmarked"}

# GET MY BOOKMARKS
@router.get("/")
def get_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id
    ).all()