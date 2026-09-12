from fastapi import FastAPI
from database import SessionLocal, engine
import models
from models import Blog

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}



models.Base.metadata.create_all(bind=engine)