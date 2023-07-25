import uvicorn
import uuid
from fastapi import FastAPI, Body, Header
from pydantic import BaseModel, EmailStr

app = FastAPI()


### In Memory Storage


users_data = []

posts_data = []


### Schema

class user(BaseModel):
    id: uuid.UUID
    email: EmailStr
    password: str
    
class post(BaseModel):
    id: uuid.UUID
    text: str
    author: str
    
class post_in(BaseModel):
    text: str


### Dependencies
def process_auth_input(
        email: str =Body(..., min_length=5, max_length=255), 
        password: str=Body(..., min_length=8)
    ):
    return {email, password}

def check_authenticated_user():
    # Validate token from header
    # Implement Dependency in route
    return True


### Auth Routes
@app.post('/signup')
def signup_user(
        email: str =Body(..., min_length=5, max_length=255), 
        password: str=Body(..., min_length=8)
    ):
    new_user = user(
        id=uuid.uuid4(),
        email=email, 
        password=password
    )
    # Check user exists
    # Create user
    users_data.append(new_user.dict())
    # Authenticate user
    # Return Token
    pass
    
@app.post('/login')
def login_user(
        email: str =Body(..., min_length=5, max_length=255), 
        password: str=Body(..., min_length=8)
    ):
    # Check email
    # Check password
    # Authenticate user
    # Return Token
    pass


### Data Routes


@app.post('/addPost')
def create_user_post(
        post_input: post_in = Body(...)
    ):
    # Check authentication
    # Get current user
    current_user = ""
    # Generate new id and Assign User
    new_post = post(
        id=uuid.uuid4(),
        text=post_input.text,
        author=current_user
    )
    # Store post in memory
    posts_data.append(new_post.dict())
    # Return id
    return {"post_id": new_post.id}


@app.get('/getPosts')
def get_user_posts():
    # Check authentication
    # Get current user
    current_user = ""
    # Get all posts, Filter posts for only current user and Return posts list
    user_posts = list(filter(lambda post_entry: post_entry['author'] == current_user , posts_data))
    return {"posts": user_posts}


### Debugging setup


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)