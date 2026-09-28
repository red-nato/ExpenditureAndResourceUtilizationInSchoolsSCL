"""Ejecuta las ocho etapas del workshop con los datos reducidos incluidos."""
from pathlib import Path
try:
    from .pipeline_la_cisterna import run
except ImportError:
    from pipeline_la_cisterna import run

ROOT = Path(__file__).resolve().parents[1]


def main():
    metrics = run(ROOT / "data", ROOT / "analysis/outputs")
    print(f"Universo anual: {metrics['universo_anual']}")
    print(f"PAS: {metrics['pas']['procesos']}; PME: {metrics['pme']['acciones']}; SIMCE: {metrics['agencia']['simce_filas']}; IDPS: {metrics['agencia']['idps_filas']}")
    return metrics


if __name__ == "__main__":
    main()
