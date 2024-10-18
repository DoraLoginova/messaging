from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    WebSocket,
    WebSocketDisconnect

)
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .auth import register_user, login_user
from .models import Message
from .pydantic_models import UserRegister, MessageCreate
from .servicedb import connect_db

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register/")
async def register(user: UserRegister, db: Session = Depends(connect_db)):
    result = await register_user(user.username, user.password, db)
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
async def send_message(
    message: MessageCreate,
    db: Session = Depends(connect_db)
):
    new_message = Message(
        sender_id=message.sender_id,
        recipient_id=message.recipient_id,
        content=message.content
    )
    db.add(new_message)
    await db.commit()
    return {"detail": "Сообщение успешно отправлено"}


@app.get("/messages/history/{user_id}")
async def get_history(user_id, db: Session = Depends(connect_db)):
    messages = await db.execute(select(Message).where(
        (Message.sender_id == user_id) | (Message.recipient_id == user_id)
    ))
    return messages.scalars().all()


@app.get("/secure-data/")
async def secure_data(token: str = Depends(oauth2_scheme)):
    return {"message": "Это защищенные данные."}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Сообщение от вас: {data}")
    except WebSocketDisconnect:
        print("Клиент отключился")
