from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)

    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    # relationships
    user = relationship("User")
    post = relationship("Post")
    replies = relationship("Comment")