from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas.auth_schema import TokenData
import os

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encode_jwt

def verify_token(token: str, credentials_exception):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
      raise credentials_exception
    token_data = TokenData(email=email)
  except JWTError:
    raise credentials_exception