from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext


SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# функции для хеширования и проверки пароля
def password_verificate(usual_password, hashed_password):
    return pwd_context.verify(usual_password, hashed_password)

# функция для создания токена
def create_token(data: dict):
    # реализация токена
    pass
