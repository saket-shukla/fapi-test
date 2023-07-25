import uvicorn
from fastapi import FastAPI, Body

app = FastAPI()

### Dependencies

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
    # Check user exists
    # Create user
    # Store password
    # Store User?
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
        post: str = Body(..., min_length=10)
    ):
    # Check authentication
    # Get current user
    # Generate new id
    # Assign User
    # Store post in memory
    # Return id
    pass

@app.get('getPosts')
def get_user_posts():
    # Check authentication
    # Get current user
    # Get all posts
    # Filter posts for only current user
    # Return posts list





# Debugging setup
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)