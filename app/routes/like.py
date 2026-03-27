from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.like import Like
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/likes", tags=["Likes"])

# LIKE / UNLIKE
@router.post("/{post_id}")
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.post_id == post_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"message": "Unliked"}

    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.add(new_like)
    db.commit()

    return {"message": "Liked"}

# COUNT LIKES
@router.get("/{post_id}")
def count_likes(post_id: int, db: Session = Depends(get_db)):
    count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"likes": count}