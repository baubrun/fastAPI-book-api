from fastapi import FastAPI, APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from db_config import SessionLocal, engine
from setup import models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books", response_model=List[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    return book


@app.post("/books")
def create_book(request: schemas.Book, db: Session = Depends(get_db)):
    new_book = models.Book(
        title=request.title,
        year=request.year,
        author_id=request.author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.post("/authors")
def create_author(request: schemas.Author, db: Session = Depends(get_db)):
    new_author = models.Author(
        first_name=request.first_name,
        last_name=request.last_name,
        created=request.created
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author
