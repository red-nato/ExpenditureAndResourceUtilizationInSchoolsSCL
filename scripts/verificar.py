"""Reejecuta todos los controles sustantivos del panel de La Cisterna."""
from pathlib import Path
from pipeline_la_cisterna import run

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    metrics = run(ROOT / "datos/extraidos/la_cisterna", ROOT / "datos/procesados/la_cisterna")
    print("Validación completa:", metrics["universo_anual"], "PAS", metrics["pas"]["procesos"])
