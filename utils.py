import functools
from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions, HTTPException


def make_json_error(e):
    """
    Converts exception to json. e.g.

    { "message": "405: Method Not Allowed" }
    """

    response = jsonify(message=str(e))
    response.status_code = (e.code
                            if isinstance(e, HTTPException)
                            else 500)
    return response


def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.keys():
        app.errorhandler(code)(make_json_error)

    # for code in default_exceptions.keys():
    #     app.error_handler_spec[None][code] = make_json_error

    return app


def catch_exceptions(logger):
    def catch_exceptions_inner(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except Exception as e:
                import traceback
                logger.error(traceback.format_exc())
                return make_json_error(e)
        return wrapper
    return catch_exceptions_inner


def success_message():
    result = {
        'message': 'success'
    }
    return jsonify(result)
