from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

# set a temp secret key, the algorithm method, and the token expiration duration
SECRET_KEY = "my-secret-key" # replace with environment var in real project or if this were to go live
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # not used at the moment, can be used in create_access_token with override

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# turn a plain password into a secure, hashed version
def hash_password(password: str):
    return pwd_context.hash(password)

# checks if a given password matches a hashed one
def verify_password(plain_password: str, hashed: str):
    return pwd_context.verify(plain_password, hashed)

# builds a JWT token that expires after ACCESS_TOKEN_EXPIRE_MINUTES minutes
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# reads and validates the token, returns the username
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload.get("sub")   # the username
    except JWTError:
        return None