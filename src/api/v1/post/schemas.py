from pydantic import BaseModel

class CreatePostSchema(BaseModel):
    title: str
    content: str
    image: bytes
    oxxo_name: str
    user_name : str

class RetrievePostSchema(BaseModel):
    id: str
    title: str
    content: str
    image_url: str
    oxxo_name: str
    user_name : str