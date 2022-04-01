from functools import wraps
from http import HTTPStatus
from typing import Callable
from flask import request


def validate_post_keys():
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            body_req = request.get_json()
            available_keys = ["anime", "released_date", "seasons"]
            missing_keys = set(available_keys).difference(body_req)
            wrong_keys = [key for key in body_req if not key in available_keys]

            try:
                if wrong_keys:
                    raise KeyError(
                        {
                            "available_keys": list(available_keys),
                            "wrong_keys_sended": list(wrong_keys),
                        }
                    )
                if missing_keys:
                    raise KeyError(
                        {
                            "available_keys": list(available_keys),
                            "wrong_keys_sended": list(missing_keys),
                        }
                    )
                return func(*args, **kwargs)
            except (KeyError, TypeError) as e:
                return e.args[0], HTTPStatus.UNPROCESSABLE_ENTITY

        return wrapper

    return decorator


def validate_patch_key():
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            body_req = request.get_json()
            available_keys = ["anime", "released_date", "seasons"]
            wrong_keys = [key for key in body_req if not key in available_keys]

            try:

                if wrong_keys:
                    raise KeyError(
                        {
                            "available_keys": list(available_keys),
                            "wrong_keys": list(wrong_keys),
                        }
                    )
                return func(*args, **kwargs)
            except (KeyError, TypeError) as e:
                return e.args[0], HTTPStatus.UNPROCESSABLE_ENTITY

        return wrapper

    return decorator
