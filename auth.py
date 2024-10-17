from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from models import User

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
TOKEN_LIFE = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_user(username, password, db):
    exist_user = await db.execute(
        select(User).where(User.username == username)
    )
    if exist_user:
        return False
    hash_password = pwd_context.hash(password)
    await db.execute(User.__table__.insert().values(
        username=username,
        password=hash_password
    ))
    return True


async def auth_user(db, username, password):
    user = await db.execute(select(User).where(User.username == username))
    if not user or not pwd_context.verify(password, user['password']):
        return False
    return user


def create_token(user_data):
    token_data = user_data.copy()
    expiration = datetime.now() + timedelta(minutes=TOKEN_LIFE)
    token_data.update({"exp": expiration})
    aggregated_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return aggregated_jwt
