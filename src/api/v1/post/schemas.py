from pydantic import BaseModel
from typing import Optional

class CreatePostSchema(BaseModel):
    title: str
    content: str
    oxxo_name: str
    user_name : str

class RetrievePostSchema(BaseModel):
    id: str
    title: str
    content: str
    image_url: Optional[str]
    oxxo_name: str
    user_name : str
    number_of_reactions : int