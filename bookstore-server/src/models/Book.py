from bson import ObjectId

from src.models.MongoObject import MongoObject

class Book(MongoObject):
    def __init__(self, _id: ObjectId, title: str, image: str, author: str, description: str, genre: str) -> None:
        super().__init__(_id=_id)
        self.__title = title
        self.__image = image
        self.__author = author
        self.__description = description
        self.__genre = genre
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def image(self) -> str:
        return self.__image
    
    @property
    def author(self) -> str:
        return self.__author
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def genre(self) -> str:
        return self.__genre
    
    def to_dict(self) -> dict[str, str]:
        return {
            "_id": str(self.id),
            "title": self.title,
            "image": self.image,
            "author": self.author,
            "description": self.description,
            "genre": self.genre,
        }
    
    def __str__(self) -> str:
        return f"\n----- BOOK START -----\n" \
        f"Id: {self.id}\n" \
        f"Title: {self.title}\n" \
        f"Image: {self.image}\n" \
        f"Author: {self.author}\n" \
        f"Description: {self.description}\n" \
        f"Genre: {self.genre}\n" \
        f"----- BOOK END -----\n"