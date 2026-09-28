"""Punto de entrada compatible: análisis activo de La Cisterna."""
from pathlib import Path
from pipeline_la_cisterna import run

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    metrics = run(ROOT / "datos/extraidos/la_cisterna", ROOT / "datos/procesados/la_cisterna")
    print("Universo anual:", metrics["universo_anual"])
    print("PAS:", metrics["pas"]["procesos"], "PME:", metrics["pme"]["acciones"])
