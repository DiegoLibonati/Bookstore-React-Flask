from pydantic import BaseModel, ConfigDict, Field


class BookModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=500)
    image: str = Field(..., min_length=1, max_length=2048)
    author: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=10000)
    genre: str = Field(..., min_length=1, max_length=100)
