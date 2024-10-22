from fastapi import HTTPException, status
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from models import User

TOKEN_LIFE = 15

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_user(username, password, db):
    print(f"Попытка регистрации пользователя: {username}")
    exist_user = await db.execute(
        select(User).where(User.username == username)
    )
    if exist_user.scalars().first():
        print(f"Пользователь {username} уже существует.")
        return False
    hash_password = pwd_context.hash(password)
    new_user = User(username=username, password=hash_password)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        print(f"Пользователь {username} успешно зарегистрирован с ID: {new_user.id}")
    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")
        await db.rollback()  # Откатить изменения при ошибке
    return True


async def login_user(db, username, password):
    res = await db.execute(select(User).where(User.username == username))
    user = res.scalars().first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )
    token_data = {"sub": user.username}
    expiration = datetime.now() + timedelta(minutes=TOKEN_LIFE)
    token_data.update({"exp": expiration})
    access_token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}
