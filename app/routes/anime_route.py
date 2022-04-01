from flask import Blueprint
from app.controllers import anime_controller

bp = Blueprint("animes", __name__, url_prefix="/animes")

bp.get("")(anime_controller.get_animes)
bp.post("")(anime_controller.add_anime)
bp.get("/<int:anime_id>")(anime_controller.get_anime_by_id)
bp.patch("/<int:anime_id>")(anime_controller.update_anime)
bp.delete("/<int:anime_id>")(anime_controller.delete_anime)
