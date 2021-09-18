from pydantic import BaseModel, constr

class BookSchema(BaseModel):
    id: int
    title: constr(max_length=20)
    year : str
    author_id : int

    class Config:
        orm_mode = False

class AuthourSchema(BaseModel):
    id: int
    first_name : str
    last_name : str
    created : str
    author_id : int

    class Config:
        orm_mode = False

