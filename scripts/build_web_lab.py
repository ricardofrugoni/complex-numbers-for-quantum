"""Exporta um laboratório Plotly autônomo; MathJax é carregado pela internet."""
import json
import base64
from pathlib import Path

import plotly.graph_objects as go
from plotly.offline import get_plotlyjs
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / "assets" / "web"
    colors = sns.color_palette(["#8fa8ff", "#f093cd", "#7acddd", "#71839f"]).as_hex()
    theme = go.Layout(template="plotly_dark", colorway=colors,
                      font=dict(family="Montserrat, sans-serif", size=11, color="#a9b9d4"),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=42, r=22, t=45, b=42),
                      legend=dict(orientation="h", x=0, y=1.13, font=dict(size=10)))
    html = (source / "lab.html").read_text(encoding="utf-8")
    def data_uri(data, mime):
        return f"data:{mime};base64," + base64.b64encode(data).decode("ascii")
    vendor = ROOT / "assets" / "vendor"
    main_module = (vendor / "three.module.min.js").read_text(encoding="utf-8")
    assert "./three.core.min.js" in main_module
    main_module = main_module.replace("./three.core.min.js", "three/core")
    imports = {"three": data_uri(main_module.encode(), "text/javascript"),
               "three/core": data_uri((vendor / "three.core.min.js").read_bytes(), "text/javascript"),
               "three/addons/controls/OrbitControls.js": data_uri((vendor / "OrbitControls.js").read_bytes(), "text/javascript")}
    for key, value in {"__STYLE__": (source / "lab.css").read_text(encoding="utf-8"),
                       "__THEME__": json.dumps(theme.to_plotly_json()),
                       "__LICENSES__": (ROOT / "assets/fonts/OFL.txt").read_text(encoding="utf-8") + "\n\n" + (vendor / "THREE-LICENSE.txt").read_text(encoding="utf-8"),
                       "__IMPORTMAP__": json.dumps({"imports": imports}),
                       "__BLOCH_MODULE__": json.dumps(data_uri((source / "bloch-three.js").read_bytes(), "text/javascript")),
                       "__FONT__": data_uri((ROOT / "assets/fonts/Montserrat-Variable.ttf").read_bytes(), "font/ttf"),
                       "__BACKGROUND__": data_uri((ROOT / "assets/backgrounds/night-sky.jpg").read_bytes(), "image/jpeg"),
                       "__SCRIPT__": (source / "lab.js").read_text(encoding="utf-8"),
                       "__PLOTLY__": get_plotlyjs()}.items():
        html = html.replace(key, value)
    output = ROOT / "docs" / "laboratorio.html"
    output.write_text(html, encoding="utf-8")
    print(f"Laboratório pronto: {output} ({output.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
