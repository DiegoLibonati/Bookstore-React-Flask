from typing import Any

from flask import Blueprint

from controllers import genres_controller


genres_route = Blueprint("genres_route", __name__)


@genres_route.route('/', methods=['GET'])
def get_all_genres() -> dict[str, Any]:
   return genres_controller.get_all_genres()


