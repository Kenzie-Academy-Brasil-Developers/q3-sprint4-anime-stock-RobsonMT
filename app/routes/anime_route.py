from flask import Blueprint
from app.controllers import anime_controller

bp = Blueprint("animes", __name__, url_prefix="/animes")

bp.get("")(anime_controller.get_animes)
bp.post("")(anime_controller.add_anime)
