from api.v1.users.schemas import (
    RequestFavorSchema
)
from firebase import firebase
from core.settings import settings
from core.utils.responses import create_envelope_response

class FirebaseFavorService:

    def __init__(self):
        self.firebase_session = firebase.FirebaseApplication(settings.FIREBASE_URL, None)

    def convertToDict(self, model: RequestFavorSchema):
        return {
            'oxxo_customer': model.oxxo_customer,
            'oxxo_friend': model.oxxo_friend,
            'latitude': model.latitude,
            'longitude': model.longitude,

        }

    def create(self, model: RequestFavorSchema):
        self.firebase_session.post("/favoare", self.convertToDict(model))
        return create_envelope_response(data=None,message=None,success=True)

