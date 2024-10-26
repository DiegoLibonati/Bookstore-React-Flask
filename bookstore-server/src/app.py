import os
from typing import Any

from flask import Flask
from flask_pymongo import PyMongo

from blueprints.v1.bookstore_route import bookstore_route


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


def load_config() -> dict[str, Any]:
    """
    Loads the initial configuration of the Flask application.

    Arguments: -

    Return: Returns a dictionary, which is the configuration of the app.
    """

    # Mongo
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config['JSON_AS_ASCII'] = False

    # API ENVS
    app.config["PORT"] = os.getenv("PORT")
    app.config["DEBUG_MODE"] = os.getenv("DEBUG_MODE")

    return app.config


def load_mongo() -> None:
    """
    Loads the initial Mongo configuration.

    Arguments: -

    Return: None
    """

    app.mongo = PyMongo(app)


def register_blueprints() -> None:
    app.register_blueprint(bookstore_route, url_prefix="/api/v1/bookstore")


def init_api() -> None:
    """
    Initializes the API.

    Arguments: -

    Return: None
    """

    # Load config API
    load_config()

    # Register blueprints
    register_blueprints()

    # Load DB - Mongo
    load_mongo()

    app.run(
        debug=app.config["DEBUG_MODE"],
        port=app.config["PORT"],
        host="0.0.0.0",
    )


if __name__ == "__main__":
    init_api()
