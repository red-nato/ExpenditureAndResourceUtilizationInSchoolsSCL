"""Extrae el censo anual de La Cisterna desde los Directorios oficiales originales.

Uso en el proyecto principal: python scripts/extraer_universo_2022_2025.py
Para otra carpeta de fuentes: --source-root /ruta/al/proyecto
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

FILES = {
    2022: "BI-DatosProyecto/Directorio/Directorio-oficial-EE-2022/20220914_Directorio_Oficial_EE_2022_20220430_WEB.csv",
    2023: "BI-DatosProyecto/Directorio/Directorio-Oficial-EE-2023-1/20230912_Directorio_Oficial_EE_2023_20230430_WEB.csv",
    2024: "BI-DatosProyecto/Directorio/Directorio-Oficial-EE-2024-/20240912_Directorio_Oficial_EE_2024_20240430_WEB.csv",
    2025: "BI-DatosProyecto/Directorio/Directorio-Oficial-EE-2025/20250926_Directorio_Oficial_EE_2025_20250430_WEB.csv",
}
REGULAR_CODES = {"110", "310", "363", "410", "510", "610", "663", "863"}
SPECIAL_CODES = {"212", "213", "214"}


def extract(source_root):
    output = []
    for year, filename in FILES.items():
        with (source_root / filename).open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter=";"):
                if row["COD_COM_RBD"] != "13109" or row["ESTADO_ESTAB"] != "1" or row["MATRICULA"] != "1":
                    continue
                if row["COD_DEPE"] not in {"2", "3", "6"} or int(row["MAT_TOTAL"]) <= 0:
                    continue
                codes = {row[f"ENS_{i:02d}"] for i in range(1, 12)} - {"0", ""}
                regular = bool(codes & REGULAR_CODES)
                special = bool(codes & SPECIAL_CODES) and not regular
                if year == 2025:
                    regular = sum(int(row[f"MAT_ENS_{i}"] or 0) for i in (2, 3, 5, 6, 7, 8)) > 0
                    special = int(row["MAT_ENS_4"] or 0) > 0 and not regular
                offer = "basica_media" if regular else "especial" if special else "revisar"
                output.append({"anio": year, "rbd": int(row["RBD"]), "nombre": row["NOM_RBD"],
                               "dependencia": {"2": "municipal_daem", "3": "particular_subvencionado", "6": "slep"}[row["COD_DEPE"]],
                               "sostenedor_rut_sin_dv": row["RUT_SOSTENEDOR"].strip() or None,
                               "matricula_total": int(row["MAT_TOTAL"]), "oferta": offer,
                               "codigos_ensenanza": sorted(codes, key=int)})
    output.sort(key=lambda row: (row["anio"], row["rbd"]))
    keys = [(r["anio"], r["rbd"]) for r in output]
    if len(keys) != len(set(keys)) or any(r["oferta"] == "revisar" for r in output):
        raise ValueError("RBD-año duplicado u oferta sin clasificar")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "datos/procesados/universo_la_cisterna_2022_2025.json")
    args = parser.parse_args()
    rows = extract(args.source_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(Counter((r["anio"], r["dependencia"]) for r in rows))
