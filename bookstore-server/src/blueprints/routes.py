from flask import Flask

from src.blueprints.v1.book_bp import book_bp


def register_routes(app: Flask) -> None:
    prefix = "/api/v1"

    app.register_blueprint(book_bp, url_prefix=f"{prefix}/books")
