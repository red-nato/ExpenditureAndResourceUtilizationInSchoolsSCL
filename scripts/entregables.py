"""Regenera el cuaderno principal y el informe PDF del workshop vigente."""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    runpy.run_path(str(ROOT / "scripts/crear_cuaderno_la_cisterna.py"), run_name="__main__")
    runpy.run_path(str(ROOT / "workshop/GROUP_03_W1/analysis/crear_cuaderno.py"), run_name="__main__")
    runpy.run_path(str(ROOT / "workshop/GROUP_03_W1/analysis/generar_informe.py"), run_name="__main__")
