"""Ejecuta el análisis principal de La Cisterna con extractos oficiales trazables."""
from pathlib import Path
from pipeline_la_cisterna import run
from integrar_chilecompra import run as integrar_chilecompra

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    integrar_chilecompra()
    metrics = run(ROOT / "datos/extraidos/la_cisterna", ROOT / "datos/procesados/la_cisterna")
    print(f"Panel anual: {metrics['universo_anual']}; PAS={metrics['pas']['procesos']}; PME={metrics['pme']['acciones']}; OC={metrics['chilecompra']['oc_seleccionadas']}")
