import os
from typing import Any

from flask import Flask
from flask_pymongo import PyMongo

from blueprints.v1.books_route import books_route
from blueprints.v1.genres_route import genres_route


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


def load_config() -> dict[str, Any]:
    # Mongo
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config['JSON_AS_ASCII'] = False

    # API ENVS
    app.config["PORT"] = os.getenv("PORT")
    app.config["DEBUG_MODE"] = os.getenv("DEBUG_MODE")

    return app.config


def load_mongo() -> None:
    app.mongo = PyMongo(app)


def register_blueprints() -> None:
    prefix = "/api/v1/bookstore"
    app.register_blueprint(books_route, url_prefix=f"{prefix}/books")
    app.register_blueprint(genres_route, url_prefix=f"{prefix}/genres")


def init_api() -> None:
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
