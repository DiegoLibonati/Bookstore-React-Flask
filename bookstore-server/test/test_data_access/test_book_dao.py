from unittest.mock import MagicMock, patch

from bson import ObjectId

from src.data_access.book_dao import BookDAO


def test_insert_one(book_test: dict[str, str]) -> None:
    mock_result = MagicMock()
    with patch("src.data_access.book_dao.mongo") as mock_mongo:
        mock_mongo.db.books.insert_one.return_value = mock_result

        result = BookDAO.insert_one(book_test)

        assert result == mock_result
        mock_mongo.db.books.insert_one.assert_called_once_with(book_test)


def test_find(book_test: dict[str, str]) -> None:
    with patch("src.data_access.book_dao.mongo") as mock_mongo:
        mock_mongo.db.books.find.return_value = [book_test]

        result = BookDAO.find()

        assert isinstance(result, list)
        assert result[0]["_id"] == str(book_test["_id"])
        assert "title" in result[0]


def test_find_by_genre(book_test: dict[str, str]) -> None:
    with patch("src.data_access.book_dao.mongo") as mock_mongo:
        mock_mongo.db.books.find.return_value = [book_test]

        result = BookDAO.find_by_genre(book_test.get("genre"))

        mock_mongo.db.books.find.assert_called_once_with(
            {"genre": book_test.get("genre")}
        )
        assert result[0]["genre"] == book_test.get("genre")


def test_find_by_id(book_test: dict[str, str]) -> None:
    with patch("src.data_access.book_dao.mongo") as mock_mongo:
        mock_mongo.db.books.find_one.return_value = book_test

        result = BookDAO.find_one_by_id(book_test["_id"])

        mock_mongo.db.books.find_one.assert_called_once_with(
            {"_id": ObjectId(book_test["_id"])}
        )
        assert result["_id"] == str(book_test["_id"])


def test_find_one_by_title_and_author(book_test: dict[str, str]) -> None:
    with patch("src.data_access.book_dao.mongo") as mock_mongo:
        mock_mongo.db.books.find_one.return_value = book_test

        result = BookDAO.find_one_by_title_and_author("Drácula", "Bram Stoker")

        mock_mongo.db.books.find_one.assert_called_once_with(
            {"title": "Drácula", "author": "Bram Stoker"}
        )
        assert result["_id"] == str(book_test["_id"])
        assert result["title"] == book_test["title"]
        assert result["author"] == book_test["author"]


def test_delete_one_by_id(book_test: dict[str, str]) -> None:
    mock_result = MagicMock()
    with patch("src.data_access.book_dao.mongo") as mock_mongo:
        mock_mongo.db.books.delete_one.return_value = mock_result

        result = BookDAO.delete_one_by_id(book_test["_id"])

        mock_mongo.db.books.delete_one.assert_called_once_with(
            {"_id": ObjectId(book_test["_id"])}
        )
        assert result == mock_result


def test_parse_books(book_test: dict[str, str]) -> None:
    books = [book_test]
    result = BookDAO.parse_books(books)

    assert isinstance(result, list)
    assert result[0]["_id"] == str(book_test["_id"])
    assert result[0]["title"] == book_test["title"]
