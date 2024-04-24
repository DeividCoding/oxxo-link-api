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
from api.v1.post.schemas import CreatePostSchema
from api.v1.post.services import CreatePostService
from sqlalchemy.orm import Session
from core.settings.database import get_session

router = APIRouter(prefix="/post", tags=["post"])


@router.post(
    "/",
    summary="Create post",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse
)
async def create(
    request: Request,
    payload: CreatePostSchema,
    session: Session = Depends(get_session)
):
    log.info("Create Post")
    return CreatePostService(session=session).create(payload=payload)


@router.get(
    "/{name}",
    summary="Create post",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse
)
async def get_post(
    name: str,
    request: Request,
    session: Session = Depends(get_session)
):
    log.info("Get Post")
    return CreatePostService(session=session).get_by_oxxo(oxxo_name=name)