from pydantic import BaseModel
from typing import Optional

class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None