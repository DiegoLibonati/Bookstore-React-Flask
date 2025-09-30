from pydantic import BaseModel


class BookModel(BaseModel):
    title: str
    image: str
    author: str
    description: str
    genre: str
