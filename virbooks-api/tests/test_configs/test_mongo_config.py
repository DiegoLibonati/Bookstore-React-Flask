from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

from src.configs.mongo_config import Mongo, init_mongo, mongo


@pytest.mark.unit
class TestMongoClass:
    def test_initial_client_is_none(self) -> None:
        m: Mongo = Mongo()
        assert m.client is None

    def test_initial_db_is_none(self) -> None:
        m: Mongo = Mongo()
        assert m.db is None

    def test_init_app_sets_client(self) -> None:
        m: Mongo = Mongo()
        app: Flask = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017"
        app.config["MONGO_DB_NAME"] = "test_db"

        with patch("src.configs.mongo_config.MongoClient") as mock_mongo_client:
            mock_client: MagicMock = MagicMock()
            mock_mongo_client.return_value = mock_client
            m.init_app(app)

        assert m.client is mock_client

    def test_init_app_sets_db_from_db_name(self) -> None:
        m: Mongo = Mongo()
        app: Flask = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017"
        app.config["MONGO_DB_NAME"] = "test_db"

        with patch("src.configs.mongo_config.MongoClient") as mock_mongo_client:
            mock_client: MagicMock = MagicMock()
            mock_db: MagicMock = MagicMock()
            mock_client.__getitem__.return_value = mock_db
            mock_mongo_client.return_value = mock_client
            m.init_app(app)

        mock_client.__getitem__.assert_called_once_with("test_db")
        assert m.db is mock_db

    def test_init_app_uses_mongo_uri_from_config(self) -> None:
        m: Mongo = Mongo()
        app: Flask = Flask(__name__)
        expected_uri: str = "mongodb://user:pass@host:27017/db"
        app.config["MONGO_URI"] = expected_uri
        app.config["MONGO_DB_NAME"] = "db"

        with patch("src.configs.mongo_config.MongoClient") as mock_mongo_client:
            mock_mongo_client.return_value = MagicMock()
            m.init_app(app)

        mock_mongo_client.assert_called_once_with(expected_uri)


@pytest.mark.unit
class TestInitMongo:
    def test_init_mongo_delegates_to_mongo_singleton(self) -> None:
        app: Flask = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017"
        app.config["MONGO_DB_NAME"] = "test_db"

        with patch.object(mongo, "init_app") as mock_init_app:
            init_mongo(app)

        mock_init_app.assert_called_once_with(app)
