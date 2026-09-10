"""Abre um laboratório local ou exporta prévias estáticas sem interface gráfica."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lab", nargs="?", default="euler3d", choices=[
        "plano", "soma", "multiplicacao", "euler3d", "potencias", "modulo3d", "amplitudes", "todos"])
    parser.add_argument("--output", type=Path, help="Diretório para PNGs estáticos; não abre janelas.")
    args = parser.parse_args()
    if args.output:
        import matplotlib
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from src.interactive_geometry import EXPLORERS

    names = EXPLORERS if args.lab == "todos" else [args.lab]
    labs = []
    for name in names:
        lab = EXPLORERS[name]()
        labs.append(lab)
        if args.output:
            args.output.mkdir(parents=True, exist_ok=True)
            destination = args.output / f"{name}.png"
            lab.fig.savefig(destination, dpi=130)
            lab.close()
            print(destination)
    if not args.output:
        backend = plt.get_backend().lower()
        if backend in {"agg", "pdf", "svg", "ps", "template", "cairo"} or "inline" in backend:
            for lab in labs:
                lab.close()
            parser.exit(1, "O backend atual é estático. Use o notebook com %matplotlib widget "
                        "ou configure um backend gráfico instalado (por exemplo, TkAgg).\n")
        plt.show()


if __name__ == "__main__":
    main()
