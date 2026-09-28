"""Regenera el cuaderno con salidas obtenidas del módulo W1."""
from pathlib import Path
import contextlib
import io
import json
import os
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
os.chdir(root)
from analysis.w1_analisis import main

out = io.StringIO()
with contextlib.redirect_stdout(out):
    main()


def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source}


def code(source, output, count):
    return {"cell_type": "code", "metadata": {}, "source": source, "execution_count": count,
            "outputs": [{"name": "stdout", "output_type": "stream", "text": output}]}


book = {"cells": [
    md("# W1 · Investigación de recursos escolares en La Cisterna\n\nGrupo 03. Se examinan 60 RBD en 2022–2023 y 59 en 2024–2025, públicos y particulares subvencionados. El análisis no estima recursos malgastados."),
    md("## Ocho etapas del flujo de datos\n\n**Load → Profile → Explore → Clean → Impute → Transform → Validate → Explore again.** El módulo aplica las etapas en ese orden. `data/PROCEDENCIA.md` documenta fuente, unidad y límites; `analysis/outputs/` conserva perfiles, controles y panel anual."),
    code("from analysis.w1_analisis import main\nmetricas = main()", out.getvalue(), 1),
    md("### Profile y Explore\n\nLa llave RBD–año se propone antes de unir. Las otras llaves son PA_ID, fila_excel, RBD–año–grado y RBD–año–grado–indicador. El perfil registra nulos y duplicados de cada una."),
    code("from pathlib import Path\nprint(Path('analysis/outputs/perfil_fuentes.csv').read_text())", (root / "analysis/outputs/perfil_fuentes.csv").read_text() + "\n", 2),
    md("### Clean, Impute, Transform y Validate\n\nLa limpieza tipa RBD, años y montos sin descartar filas. No se imputan rendiciones, montos ni puntajes; solo se contabilizan cero filas publicadas y se conserva una marca de presencia. Cada fuente se agrega por RBD antes del join. Las aserciones comprueban llaves y conservación."),
    code("print(Path('analysis/outputs/controles_etapas.csv').read_text())", (root / "analysis/outputs/controles_etapas.csv").read_text() + "\n", 3),
    md("### Explore again\n\nEl censo anual muestra el RBD 9830 solo en 2022–2023. Las tablas de Agencia conservan año, grado y versiones; una fila sin puntaje no se confunde con un resultado. Las acciones PME son estimaciones declaradas y PAS no identifica por sí solo un gasto financiero irregular."),
    code("print(Path('analysis/outputs/universo_anual.csv').read_text())\nprint(Path('analysis/outputs/cobertura_agencia_por_grado.csv').read_text())", (root / "analysis/outputs/universo_anual.csv").read_text() + "\n" + (root / "analysis/outputs/cobertura_agencia_por_grado.csv").read_text() + "\n", 4),
], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
path = root / "analysis/W1_analisis_ejecutado.ipynb"
path.write_text(json.dumps(book, ensure_ascii=False, indent=1), encoding="utf-8")
print(path)
