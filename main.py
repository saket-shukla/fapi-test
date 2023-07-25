import uvicorn
import uuid
from datetime import datetime, timedelta
from fastapi import FastAPI, Body, Header, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "nsjnjna3289sjnjansjnjnndsjnajnjdnasn"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


### In Memory Storage


users_data = []

posts_data = []


### Schema


class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    email: str | None = None
    

class User(BaseModel):
    id: uuid.UUID
    email: EmailStr
    password: str
    
    
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, email: str):
    for user_entry in db:
        if user_entry['email'] == email:
            return User(**user_entry)
    return None

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(users_data, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user   

def authenticate_user(fake_db, email: str, password: str):
    user = get_user(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
    
class Post(BaseModel):
    id: uuid.UUID
    text: str
    author: str
    
class PostIn(BaseModel):
    text: str


### Auth Routes
@app.post('/signup')
def signup_user(
        email: str =Body(..., min_length=5, max_length=255), 
        password: str=Body(..., min_length=8)
    ):
    new_user = User(
        id=uuid.uuid4(),
        email=email, 
        password=get_password_hash(password)
    )
    # Check user exists
    # Create user
    users_data.append(new_user.dict())
    # Return Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    
@app.post('/login')
def login_user(
        email: str =Body(..., min_length=5, max_length=255), 
        password: str=Body(..., min_length=8)
    ):
    # Authenticate user
    user = authenticate_user(users_data, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Return Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


### Data Routes


@app.post('/addPost')
def create_user_post(
        post_input: PostIn = Body(...),
        current_user: User | None = Depends(get_current_user)
    ):
    # Generate new id and Assign User
    new_post = Post(
        id=uuid.uuid4(),
        text=post_input.text,
        author=current_user
    )
    # Store post in memory
    posts_data.append(new_post.dict())
    # Return id
    return {"post_id": new_post.id}


@app.get('/getPosts')
def get_user_posts(
        current_user: User | None = Depends(get_current_user)
    ):
    # Get all posts, Filter posts for only current user and Return posts list
    user_posts = list(filter(lambda post_entry: post_entry['author'] == current_user , posts_data))
    return {"posts": user_posts}


### Debugging setup


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)