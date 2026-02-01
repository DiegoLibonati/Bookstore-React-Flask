import pytest
from pydantic import ValidationError

from src.models.book_model import BookModel


class TestBookModelCreation:
    def test_create_valid_book(self) -> None:
        book = BookModel(
            title="Drácula",
            image="dracula.jpg",
            author="Bram Stoker",
            description="A gothic horror novel",
            genre="Horror",
        )

        assert book.title == "Drácula"
        assert book.image == "dracula.jpg"
        assert book.author == "Bram Stoker"
        assert book.description == "A gothic horror novel"
        assert book.genre == "Horror"

    def test_model_dump_returns_dict(self) -> None:
        book = BookModel(
            title="Test",
            image="test.jpg",
            author="Author",
            description="Description",
            genre="Genre",
        )

        result = book.model_dump()

        assert isinstance(result, dict)
        assert result == {
            "title": "Test",
            "image": "test.jpg",
            "author": "Author",
            "description": "Description",
            "genre": "Genre",
        }


class TestBookModelRequiredFields:
    def test_title_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            BookModel(
                image="test.jpg",
                author="Author",
                description="Description",
                genre="Genre",
            )

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("title",) for e in errors)

    def test_image_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            BookModel(
                title="Title", author="Author", description="Description", genre="Genre"
            )

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("image",) for e in errors)

    def test_author_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            BookModel(
                title="Title",
                image="test.jpg",
                description="Description",
                genre="Genre",
            )

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("author",) for e in errors)

    def test_description_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            BookModel(title="Title", image="test.jpg", author="Author", genre="Genre")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("description",) for e in errors)

    def test_genre_is_required(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            BookModel(
                title="Title",
                image="test.jpg",
                author="Author",
                description="Description",
            )

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("genre",) for e in errors)

    def test_empty_model_fails(self) -> None:
        with pytest.raises(ValidationError):
            BookModel()


class TestBookModelMinLength:
    def test_title_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="",
                image="test.jpg",
                author="Author",
                description="Description",
                genre="Genre",
            )

    def test_image_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="Title",
                image="",
                author="Author",
                description="Description",
                genre="Genre",
            )

    def test_author_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="Title",
                image="test.jpg",
                author="",
                description="Description",
                genre="Genre",
            )

    def test_description_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="Title",
                image="test.jpg",
                author="Author",
                description="",
                genre="Genre",
            )

    def test_genre_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="Title",
                image="test.jpg",
                author="Author",
                description="Description",
                genre="",
            )

    def test_single_character_is_valid(self) -> None:
        book = BookModel(title="A", image="B", author="C", description="D", genre="E")

        assert book.title == "A"
        assert book.image == "B"
        assert book.author == "C"
        assert book.description == "D"
        assert book.genre == "E"


class TestBookModelStripWhitespace:
    def test_title_strips_whitespace(self) -> None:
        book = BookModel(
            title="  Spaced Title  ",
            image="test.jpg",
            author="Author",
            description="Description",
            genre="Genre",
        )

        assert book.title == "Spaced Title"

    def test_image_strips_whitespace(self) -> None:
        book = BookModel(
            title="Title",
            image="  spaced.jpg  ",
            author="Author",
            description="Description",
            genre="Genre",
        )

        assert book.image == "spaced.jpg"

    def test_author_strips_whitespace(self) -> None:
        book = BookModel(
            title="Title",
            image="test.jpg",
            author="  Spaced Author  ",
            description="Description",
            genre="Genre",
        )

        assert book.author == "Spaced Author"

    def test_description_strips_whitespace(self) -> None:
        book = BookModel(
            title="Title",
            image="test.jpg",
            author="Author",
            description="  Spaced Description  ",
            genre="Genre",
        )

        assert book.description == "Spaced Description"

    def test_genre_strips_whitespace(self) -> None:
        book = BookModel(
            title="Title",
            image="test.jpg",
            author="Author",
            description="Description",
            genre="  Spaced Genre  ",
        )

        assert book.genre == "Spaced Genre"

    def test_only_whitespace_fails(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="   ",
                image="test.jpg",
                author="Author",
                description="Description",
                genre="Genre",
            )


class TestBookModelNoneValues:
    def test_title_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title=None,
                image="test.jpg",
                author="Author",
                description="Description",
                genre="Genre",
            )

    def test_image_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="Title",
                image=None,
                author="Author",
                description="Description",
                genre="Genre",
            )

    def test_author_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="Title",
                image="test.jpg",
                author=None,
                description="Description",
                genre="Genre",
            )

    def test_description_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="Title",
                image="test.jpg",
                author="Author",
                description=None,
                genre="Genre",
            )

    def test_genre_none_fails(self) -> None:
        with pytest.raises(ValidationError):
            BookModel(
                title="Title",
                image="test.jpg",
                author="Author",
                description="Description",
                genre=None,
            )


class TestBookModelSpecialCharacters:
    def test_title_with_special_characters(self) -> None:
        special_titles = [
            "El señor de los anillos",
            "日本語タイトル",
            "Title: Part 1 - The Beginning",
            "Book (2024 Edition)",
            "100% Pure Fiction",
        ]

        for title in special_titles:
            book = BookModel(
                title=title,
                image="test.jpg",
                author="Author",
                description="Description",
                genre="Genre",
            )
            assert book.title == title

    def test_author_with_special_characters(self) -> None:
        special_authors = [
            "José García",
            "O'Brien",
            "Mary-Jane Watson",
            "Author Jr.",
            "Müller",
        ]

        for author in special_authors:
            book = BookModel(
                title="Title",
                image="test.jpg",
                author=author,
                description="Description",
                genre="Genre",
            )
            assert book.author == author


class TestBookModelSerialization:
    def test_model_to_json(self) -> None:
        book = BookModel(
            title="Test Book",
            image="test.jpg",
            author="Test Author",
            description="Test Description",
            genre="Test Genre",
        )

        json_str = book.model_dump_json()

        assert "Test Book" in json_str
        assert "test.jpg" in json_str
        assert "Test Author" in json_str

    def test_model_from_dict(self) -> None:
        data = {
            "title": "From Dict",
            "image": "dict.jpg",
            "author": "Dict Author",
            "description": "Dict Description",
            "genre": "Dict Genre",
        }

        book = BookModel(**data)

        assert book.title == "From Dict"
        assert book.author == "Dict Author"

    def test_model_ignores_extra_fields(self) -> None:
        book = BookModel(
            title="Title",
            image="test.jpg",
            author="Author",
            description="Description",
            genre="Genre",
            extra_field="ignored",
        )

        assert book.title == "Title"
        assert not hasattr(book, "extra_field")
