"""Fonte local compartilhada pelas figuras; não instala fontes no sistema."""
from pathlib import Path
from functools import cache

from matplotlib import font_manager

FONT_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"


@cache
def register_montserrat():
    for path in FONT_DIR.glob("Montserrat-*.ttf"):
        font_manager.fontManager.addfont(path)
    return ["Montserrat", "DejaVu Sans"]
