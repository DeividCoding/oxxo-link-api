from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
    File,
    UploadFile,
    Form,
    HTTPException
)
import json
from core.utils.responses import (
    EnvelopeResponse,
)
from core.settings import log
from api.v1.post.schemas import CreatePostSchema
from api.v1.post.services import CreatePostService
from sqlalchemy.orm import Session
from core.settings.database import get_session
from uuid import UUID
from typing import Optional


router = APIRouter(prefix="/post", tags=["post"])

@router.post(
    "/",
    summary="Create post",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse
)
async def create(
    title: str,
    content: str,
    oxxo_name: str,
    user_name:str,
    #image: UploadFile = [File(...)],
    session: Session = Depends(get_session)
):
    image = None
    log.info("Create Post")
    return CreatePostService(session=session).create(
        CreatePostSchema(
            title=title,
            content=content,
            oxxo_name=oxxo_name,
            user_name=user_name
        ),
        image=image
    )
@router.patch(
    "/like/{post_id}",
    summary="Give like to post",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse
)
async def like(
    post_id: UUID,
    request: Request,
    session: Session = Depends(get_session)
):
    log.info("Give like")
    return CreatePostService(session=session).give_like(post_id=post_id)

@router.patch(
    "/unlike/{post_id}",
    summary="Give unlike to post",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse
)
async def unlike(
    post_id: UUID,
    request: Request,
    session: Session = Depends(get_session)
):
    log.info("Give unlike")
    return CreatePostService(session=session).give_unlike(post_id=post_id)



@router.get(
    "/{oxxo_name}",
    summary="Get  post by oxxo_name",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse
)
async def get_post(
    oxxo_name: str,
    request: Request,
    session: Session = Depends(get_session)
):
    log.info("Get Post")
    return CreatePostService(session=session).get_by_oxxo(oxxo_name=oxxo_name)