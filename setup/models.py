from db_config import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created = Column(String(50))

    books = relationship("Book",
                         back_populates="author",
                         )

    def __repr__(self):
        return f'<Author(id="{self.id}", ' \
               f'first_name="{self.first_name}", ' \
               f'last_name="{self.last_name}", ' \
               f'created="{self.created}")' \
               f'author_id="{self.author.id}>'


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    year = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author",
                          back_populates="books"
                          )

    def __repr__(self):
        return f'<Book(id="{self.id}", ' \
               f'title="{self.title}", ' \
               f'year="{self.year}", ' \
               f'author_id="{self.author_id}")>'
