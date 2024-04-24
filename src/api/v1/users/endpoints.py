from fastapi import (
    APIRouter,
    Depends,
    status,
    Request
)
from core.utils.responses import (
    EnvelopeResponse,
)
from core.settings import log
from api.v1.users.schemas import RequestFavorSchema
from api.v1.users.services import FirebaseFavorService
from sqlalchemy.orm import Session
from core.settings.database import get_session


router = APIRouter(prefix="/users", tags=["post"])


@router.post(
    "/favoare",
    summary="Update",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse
)
async def create_favor(sensors: RequestFavorSchema):
    controller_firebase = FirebaseFavorService()
    return controller_firebase.create(sensors)