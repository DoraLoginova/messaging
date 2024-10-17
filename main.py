from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .auth import register_user, login_user
from .servicedb import connect_db

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register/")
async def register(username, password, db: Session = Depends(connect_db)):
    result = await register_user(username, password, db)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже существует"
        )
    return {"detail": "Пользователь успешно зарегистрирован"}


@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(connect_db)
):
    return await login_user(db, form_data.username, form_data.password)


@app.post("/messages/")
async def send_message(message: Message, db: Session = Depends(connect_db)):
    # Логика для отправки сообщения
    pass

@app.get("/messages/history/{user_id}")
async def get_history(user_id: int, db: Session = Depends(get_db)):
    # Логика для извлечения истории сообщений
    pass

