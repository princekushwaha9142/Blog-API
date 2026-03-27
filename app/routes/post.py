from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.post import Post
from app.schemas.post import PostCreate
from app.core.security import get_current_user
from app.models.user import User

# AI imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os

router = APIRouter(prefix="/posts", tags=["Posts"])


# =========================
# ✅ CREATE POST
# =========================
@router.post("/")
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_post = Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"message": "Post created", "post_id": new_post.id}


# =========================
# ✅ GET ALL POSTS
# =========================
@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


# =========================
# ✅ GET SINGLE POST
# =========================
@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


# =========================
# ✅ UPDATE POST
# =========================
@router.put("/{post_id}")
def update_post(
    post_id: int,
    updated_post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    post.title = updated_post.title
    post.content = updated_post.content

    db.commit()
    return {"message": "Post updated"}


# =========================
# ✅ DELETE POST
# =========================
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(post)
    db.commit()

    return {"message": "Post deleted"}


# =========================
# 🔎 SEARCH POSTS
# =========================
@router.get("/search/")
def search_posts(
    search: str = "",
    db: Session = Depends(get_db)
):
    posts = db.query(Post).filter(
        Post.title.ilike(f"%{search}%")
    ).all()

    return posts


# =========================
# 🔎 FILTER POSTS
# =========================
@router.get("/filter/")
def filter_posts(
    user_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Post)

    if user_id:
        query = query.filter(Post.owner_id == user_id)

    return query.all()


# =========================
# 📊 ANALYTICS
# =========================
@router.get("/analytics/")
def post_analytics(db: Session = Depends(get_db)):
    total_posts = db.query(Post).count()

    return {
        "total_posts": total_posts
    }


# =========================
# 📁 IMAGE UPLOAD
# =========================
@router.post("/upload/")
def upload_image(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    return {"filename": file.filename}


# =========================
# 🤖 AI RECOMMENDATION
# =========================
@router.get("/recommend/{post_id}")
def recommend_posts(post_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).all()

    if not posts:
        return []

    titles = [p.title for p in posts]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(titles)

    similarity = cosine_similarity(vectors)

    # find index safely
    index = None
    for i, p in enumerate(posts):
        if p.id == post_id:
            index = i
            break

    if index is None:
        raise HTTPException(status_code=404, detail="Post not found")

    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommended = [posts[i[0]] for i in scores[1:4]]

    return recommended