from pydantic import BaseModel, constr
from typing import Optional

class Book(BaseModel):
    id: Optional[int]
    title: constr(max_length=20)
    year : str
    author_id : int

    class Config:
        orm_mode = True

class Author(BaseModel):
    id: Optional[int]
    first_name : str
    last_name : str
    created : str

    class Config:
        orm_mode = True

