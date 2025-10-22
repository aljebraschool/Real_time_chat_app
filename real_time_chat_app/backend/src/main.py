from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.routers import auth
from src.routers import auth, messages, groups, websocket

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Real-time Chat Application API",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS middleware - allows frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(messages.router)  
app.include_router(groups.router)
app.include_router(websocket.router)


@app.get("/")
def root():
    """
    Root endpoint - health check.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    return {
        "message": "Real-time Chat API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)