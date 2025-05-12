from fastapi import FastAPI
from app.core.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.routers import users, posts, comments, likes, favorites

# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(favorites.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Social Network API"}

# Add startup event to create tables if they don't exist
@app.on_event("startup")
def startup_event():
    # Import here to avoid circular imports
    from app.core.database import Base, engine
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
