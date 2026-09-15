from fastapi import FastAPI,Depends,HTTPException,status
from database import SessionLocal, engine
import models,schemas
from models import Blog
from sqlalchemy.orm import Session
from schemas import BlogCreate,BlogResponse
from auth import create_token,verify_token

app = FastAPI()

#DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}



models.Base.metadata.create_all(bind=engine)

@app.post("/login")
def login():
    return {
        "access_token" : create_token({"sub":"admin","role":"admin"}),
        "token_type" : "bearer"
    }   

#Cleate Blog
@app.post("/blogs",response_model=schemas.BlogResponse,status_code=status.HTTP_201_CREATED)
def create_blog(blog:schemas.BlogCreate,db:Session = Depends(get_db),user = Depends(verify_token)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content,
    )

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blogs",response_model=list[schemas.BlogResponse],status_code=status.HTTP_200_OK)
def read_blogs(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blogs/{blog_id}",response_model=schemas.BlogResponse,status_code=status.HTTP_200_OK)
def read_blog(blog_id:int,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog not found")
    return blog

@app.put("/blogs/{blog_id}",response_model=schemas.BlogResponse,status_code=status.HTTP_200_OK)
def update_blog(blog_id:int,blog:schemas.BlogCreate,db:Session = Depends(get_db),user = Depends(verify_token)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not existing_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog not found")
    
    existing_blog.title = blog.title
    existing_blog.content = blog.content
    db.commit()
    db.refresh(existing_blog)
    return existing_blog

@app.delete("/blogs/{blog_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id:int,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog not found")
    
    db.delete(blog)
    db.commit()
    return {"message":"Blog deleted successfully"}