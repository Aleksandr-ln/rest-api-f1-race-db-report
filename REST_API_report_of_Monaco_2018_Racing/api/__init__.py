from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")

from .routes import api_bp  # noqa: E402

__all__ = ["api_bp"]
