from fastapi import FastAPI, APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from db_config import SessionLocal, engine
from setup import models, schemas

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


@app.get("/books")
def get_all_books():
    return {"data": [1,2,]}


@app.get("/books/{id}")
def get_book(id: int):
    return {"book": 1}

@app.post("/books")
def create_book(book: schemas.BookSchema):
    return {"data": f"Book {book.title} created!"}