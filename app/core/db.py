"""
Alias de compatibilidad: expone get_session para routers nuevos.
Ajusta el import al archivo real donde está tu get_session.
"""

# OPCIÓN A (la más común): si get_session está en app/db.py
from app.db import get_session  # noqa: F401
