from functools import wraps
from http import HTTPStatus
from typing import Callable
from flask import request
from psycopg2.errors import UniqueViolation

from app.models.anime_model import Anime


def get_animes():
    animes = Anime.select_all()
    return {"data": animes}


@validate_keys()
def add_anime():
    data = request.get_json()

    anime = Anime(**data)
    try:
        inserted_anime = anime.insert_into()
    except UniqueViolation:
        return {"error": "anime already in stock"}, HTTPStatus.UNPROCESSABLE_ENTITY

    print("#" * 20)
    print(inserted_anime)
    print("#" * 20)

    return inserted_anime, HTTPStatus.CREATED
