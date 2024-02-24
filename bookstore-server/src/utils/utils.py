from flask import make_response


def not_accepted() -> tuple:
    response = {
        'message': "I cant add this book because there is a problem",
        'status': 406
    }

    response.status_code = 406

    return make_response(
        response,
    406)