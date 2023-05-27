import os

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import UserDb

load_dotenv()

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET request that returns the current user's information.
        It requires authentication, and it uses the auth_service to get the current user.

    :param current_user: User: Tell fastapi that the function depends on a user object
    :return: The current user, which is the user that
    """

    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The image to be uploaded as an avatar.
            current_user (User): The currently logged in user, who is updating their avatar.
                This is passed by the auth_service dependency and its get_current_user function, which returns a User object
                representing the currently logged in user based on their JWT token stored in cookies or headers.

    :param file: UploadFile: Get the file from the request body
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: The updated user
    """

    cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
            secure=True
        )

    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{current_user.username}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
