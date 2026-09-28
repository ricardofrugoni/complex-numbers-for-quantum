"""Deriva os pesos de Montserrat para Matplotlib a partir da fonte OFL local."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1] / "assets" / "fonts"


if __name__ == "__main__":
    for weight, name in [(400, "Regular"), (600, "SemiBold")]:
        font = TTFont(ROOT / "Montserrat-Variable.ttf")
        instance = instantiateVariableFont(font, {"wght": weight}, inplace=True)
        instance.save(ROOT / f"Montserrat-{name}.ttf")
        print(f"Montserrat {name}: pronta")
