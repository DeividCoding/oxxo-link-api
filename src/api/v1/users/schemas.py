from pydantic import BaseModel

class RequestFavorSchema(BaseModel):
    oxxo_customer: str
    oxxo_friend: str
    latitude: float
    longitude: float
