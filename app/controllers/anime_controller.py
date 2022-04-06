from http import HTTPStatus
from flask import request
from psycopg2.errors import UniqueViolation, UndefinedTable

from app.controllers.anime_decorator_validates import (
    validate_patch_key,
    validate_post_keys,
)
from app.controllers.exc import missingKeysError
from app.models.anime_model import Anime


def get_animes():
    animes = Anime.select_all()
    return {"data": animes}


# @validate_post_keys()
def add_anime():
    data = request.get_json()

    anime = Anime(**data)
    missing_keys = set(anime.allowed_keys).difference(data)
    wrong_keys = [key for key in data if not key in anime.allowed_keys]

    try:
        if missing_keys:
            raise missingKeysError(anime.allowed_keys, missing_keys)
        inserted_anime = anime.insert_into()
    except UniqueViolation:
        return {"error": "anime in already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY

    return inserted_anime, HTTPStatus.CREATED


def get_anime_by_id(anime_id: int):
    try:
        anime = Anime.select_by_id(anime_id)
        if not anime:
            raise IndexError
    except (IndexError, UndefinedTable):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    return {"data": [anime]}


# @validate_patch_key()
def update_anime(anime_id: int):
    data = request.get_json()

    try:
        updated_anime = Anime.update_by_id(anime_id, data)
        if not updated_anime:
            raise IndexError
    except (IndexError, UndefinedTable):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    except UniqueViolation:
        return {"error": "anime in already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY

    return updated_anime


def delete_anime(anime_id: int):
    try:
        deleted_anime = Anime.delete_by_id(anime_id)
        if not deleted_anime:
            raise IndexError
    except (IndexError, UndefinedTable):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    return "", HTTPStatus.NO_CONTENT
