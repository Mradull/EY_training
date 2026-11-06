from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models
from app.routes.meetings import router as meetings_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="MeetFlow MoM Generator API",
    description="Backend API for the Minutes of Meeting Generator",
    version="1.0.0",
)


# Allow requests from the React development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register meetings routes
app.include_router(meetings_router)


@app.get("/")
def root():
    return {
        "message": "MeetFlow MoM Generator API is running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MeetFlow API",
    }