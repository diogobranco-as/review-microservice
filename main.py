from fastapi import FastAPI
from database import engine, Base
from routes import router

app = FastAPI(title="Review Microservice")

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Review Microservice is running!"}