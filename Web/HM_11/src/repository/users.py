import logging

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        logging.error(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()

# {
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbmRyaXkuQGdtYWlsLmNvbSIsImlhdCI6MTY4MzgwMjQ3OSwiZXhwIjoxNjgzODA2MDc5LCJzY29wZSI6ImFjY2Vzc190b2tlbiJ9.F4WQfcT2UMokt1wLfjqqGDVcbEQMuSpt5-V5CC9e2ks",
#     "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbmRyaXkuQGdtYWlsLmNvbSIsImlhdCI6MTY4MzgwMjQ3OSwiZXhwIjoxNjg0NDA3Mjc5LCJzY29wZSI6InJlZnJlc2hfdG9rZW4ifQ.vriH76DlOAP8xNaY1cJBYNryuKCVe3L6C4e5xJOqUqA",
#     "token_type": "bearer"
# }
