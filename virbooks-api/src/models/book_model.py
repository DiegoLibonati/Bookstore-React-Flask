from typing import Annotated

from pydantic import BaseModel, StringConstraints

ConstrainedStr = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]


class BookModel(BaseModel):
    title: ConstrainedStr
    image: ConstrainedStr
    author: ConstrainedStr
    description: ConstrainedStr
    genre: ConstrainedStr
