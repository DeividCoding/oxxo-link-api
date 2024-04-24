from api.v1.post.schemas import (
    CreatePostSchema,
    RetrievePostSchema
)
from api.v1.post.proxies import RepositoryPost
from core.utils.responses import create_envelope_response
import cloudinary.uploader
from core.settings import settings
from openai import OpenAI
from sqlalchemy import select

from models.post import PostModel


class CreatePostService():

    def __init__(self, session):
        self.session = session
        self.repository_post = RepositoryPost(session=session)
        self.client_open_ai = OpenAI(api_key=settings.OPEN_AI_API_KEY,)

    def validate_content(self,message: str):
        response = self.client_open_ai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
            {"role": "user", "content": "Hola te enviare un texto que esta conformado por un TITULO de la aplicacion y un CONTENIDO de la aplicacion y me diras si este es ofensivo o crees que deba publicarse en una app como post si es ofesivo dime 1 so no lo es dime 0 y por $$$ separa el porque es ofensivo o inadecuado"},
            {"role": "system", "content": "Claro yo te dire si es ofensivo respondiendo con un 1 o si no lo es con un 0"},
            {"role": "user", "content": message}
            ]
        )
        return tuple(response.choices[0].message.content.split("$$$"))

    def upload_image(self, image_binary):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )
        upload_result = cloudinary.uploader.upload("roni.jpg")
        image_url = upload_result['secure_url']
        return image_url

    def create(self, payload: CreatePostSchema):
        image_binary = payload.image
        image_url = self.upload_image(image_binary)
        text_content = f"TITULO PUBLICACION:{payload.title}  CONTENIDO APLICACION:{payload.content}"
        response_status = self.validate_content(message=text_content)

        if response_status[0].startswith("0"):
            post_created = self.repository_post.add(
                image_url=image_url,
                **payload.model_dump(exclude={"image"}),
                number_of_reactions=0
            )
            post_schema = RetrievePostSchema(
                id=str(post_created.id),
                title=post_created.title,
                content=post_created.content,
                image_url=post_created.image_url,
                oxxo_name= post_created.oxxo_name,
                user_name=post_created.user_name,
                number_of_reactions=post_created.number_of_reactions
            )
            return create_envelope_response(data=post_schema,message=None,success=True)
        else:
            response_message = response_status[1]
            return create_envelope_response(data=None,message=response_message,success=False)

    def get_by_oxxo(self, oxxo_name):
        data: list[PostModel] = self.repository_post.get_by_attributes(oxxo_name=oxxo_name)
        return create_envelope_response(data=[d.as_dict() for d in data],message=None,success=True)
    
    def give_like(self,post_id):
        post = self.repository_post.get_by_id(post_id)
        post.number_of_reactions+= 1
        self.session.commit()
        post_schema = RetrievePostSchema(
            id=str(post.id),
            title=post.title,
            content=post.content,
            image_url=post.image_url,
            oxxo_name= post.oxxo_name,
            user_name=post.user_name,
            number_of_reactions=post.number_of_reactions
        )
        return create_envelope_response(data=post_schema,message=None,success=True)

    def give_unlike(self,post_id):
        post = self.repository_post.get_by_id(post_id)
        if post.number_of_reactions>0:
            post.number_of_reactions-= 1
            self.session.commit()
            post_schema = RetrievePostSchema(
                id=str(post.id),
                title=post.title,
                content=post.content,
                image_url=post.image_url,
                oxxo_name= post.oxxo_name,
                user_name=post.user_name,
                number_of_reactions=post.number_of_reactions
            )
            return create_envelope_response(data=post_schema,message=None,success=True)