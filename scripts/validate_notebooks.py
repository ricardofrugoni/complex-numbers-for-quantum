"""Executa notebooks isolados; opcionalmente salva saídas dos notebooks estáticos."""

import argparse
import json
from pathlib import Path
import sys
from importlib.metadata import version

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="JSON opcional com os resultados da execução.")
    parser.add_argument("--save-static", action="store_true",
                        help="Salva as saídas somente dos notebooks sem widgets para leitura no GitHub.")
    args = parser.parse_args()
    results = []
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        manager = KernelManager(kernel_name="python3")
        # Garante o mesmo interpretador, mesmo se o PATH aponta a outro Python.
        manager.kernel_spec.argv[0] = sys.executable
        client = NotebookClient(notebook, km=manager, timeout=180,
                                resources={"metadata": {"path": str(path.parent)}})
        try:
            with client.setup_kernel():
                client.execute()
            count = sum(cell.cell_type == "code" for cell in notebook.cells)
            widget_views = sum("application/vnd.jupyter.widget-view+json" in output.get("data", {})
                               for cell in notebook.cells if cell.cell_type == "code"
                               for output in cell.get("outputs", []))
            expected = {"06_laboratorio_interativo.ipynb": 7,
                        "07_raizes_ondas_fourier.ipynb": 3}.get(path.name, 0)
            if widget_views < expected:
                raise RuntimeError(f"{path.name}: esperadas {expected} saídas interativas; obtidas {widget_views}.")
            if args.save_static and widget_views == 0:
                nbformat.write(notebook, path)
            results.append({"notebook": path.name, "status": "ok", "code_cells": count,
                            "widget_views": widget_views})
            print(f"OK: {path.name} ({count} células de código)", flush=True)
        finally:
            # Com km fornecido, o cliente não assume sua propriedade.
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
            manager.cleanup_resources()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        packages = {name: version(name) for name in ["numpy", "matplotlib", "jupyterlab",
                    "pytest", "ipympl", "ipywidgets", "nbclient", "nbformat"]}
        args.output.write_text(json.dumps({"python": sys.version, "packages": packages, "results": results},
                                         indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
