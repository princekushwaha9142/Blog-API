from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.user import User
from app.routes import auth, user, post
from app.routes import comment
from app.models.comment import Comment
from app.models.like import Like
from app.models.bookmark import Bookmark
from app.routes import like, bookmark


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(like.router)
app.include_router(bookmark.router)

@app.get("/")
def root():
    return {"message": "Blog API Running "}