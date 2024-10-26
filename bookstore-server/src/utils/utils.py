from flask import make_response


def not_accepted() -> tuple:
    return make_response({
        'message': "I cant add this book because there is a problem",
        'status': 406
    }, 406)