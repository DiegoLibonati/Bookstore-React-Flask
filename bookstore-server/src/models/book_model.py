from pydantic import BaseModel, constr


class BookModel(BaseModel):
    title: constr(min_length=1, strip_whitespace=True)
    image: constr(min_length=1, strip_whitespace=True)
    author: constr(min_length=1, strip_whitespace=True)
    description: constr(min_length=1, strip_whitespace=True)
    genre: constr(min_length=1, strip_whitespace=True)
