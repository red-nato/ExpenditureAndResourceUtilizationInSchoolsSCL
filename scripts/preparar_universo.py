"""Construye el censo escolar y extrae los procesos publicados de La Cisterna.

Uso: Python con openpyxl instalado. Los archivos originales se conservan sin editar.
"""

import csv
import io
import json
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "datos" / "originales"
OUT = ROOT / "datos" / "procesados"
OUT.mkdir(parents=True, exist_ok=True)


def directorio(anio, archivo):
    with (ORIG / archivo).open(encoding="utf-8-sig", newline="") as fh:
        rows = csv.DictReader(fh, delimiter=";")
        for row in rows:
            if row["COD_COM_RBD"] != "13109":
                continue
            if row["ESTADO_ESTAB"] != "1" or row["MATRICULA"] != "1":
                continue
            if row["COD_DEPE"] not in {"2", "3", "6"}:
                continue
            niveles = {row[f"ENS_{i:02d}"] for i in range(1, 12)} - {"0", ""}
            if anio == 2025:
                basica_media = sum(int(row[f"MAT_ENS_{i}"] or 0) for i in (2, 3, 5, 6, 7, 8)) > 0
                especial = int(row["MAT_ENS_4"] or 0) > 0 and not basica_media
            else:
                basica_media = bool(niveles & {"110", "310", "363", "410", "510", "610", "663", "863"})
                especial = bool(niveles & {"212", "213", "214"}) and not basica_media
            yield {
                "anio": anio,
                "rbd": int(row["RBD"]),
                "nombre": row["NOM_RBD"],
                "dependencia": {"2": "municipal_daem", "3": "particular_subvencionado", "6": "slep"}[row["COD_DEPE"]],
                "sostenedor_rut_sin_dv": row["RUT_SOSTENEDOR"].strip() or None,
            "matricula_total": int(row["MAT_TOTAL"]),
            "matricula_basica_media": (
                sum(int(row[f"MAT_ENS_{i}"] or 0) for i in (2, 3, 5, 6, 7, 8))
                if anio == 2025 else None
            ),
            "matricula_especial": int(row["MAT_ENS_4"] or 0) if anio == 2025 else None,
                "oferta": "basica_media" if basica_media else "especial" if especial else "revisar",
                "codigos_ensenanza": sorted(niveles, key=int),
            }


universe = sorted(
    [*directorio(2024, "directorio_2024.csv"),
     *directorio(2025, "20250926_Directorio_Oficial_EE_2025_20250430_WEB.csv")],
    key=lambda r: (r["anio"], r["rbd"]),
)
assert len({(r["anio"], r["rbd"]) for r in universe}) == len(universe)
assert all(r["oferta"] != "revisar" for r in universe)
(OUT / "universo_la_cisterna_2024_2025.json").write_text(
    json.dumps(universe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
rows_2025 = [r for r in universe if r["anio"] == 2025]
lines = [
    "# Universo de establecimientos de La Cisterna, 2025",
    "",
    "Directorio Oficial Mineduc 2025, corte de matrícula al 30 de abril. Incluye establecimientos funcionando, con matrícula y dependencia SLEP o particular subvencionada.",
    "",
    "| RBD | Establecimiento | Dependencia | Oferta | Matrícula total | Matrícula básica/media |",
    "|---:|---|---|---|---:|---:|",
]
for r in rows_2025:
    lines.append(
        f"| {r['rbd']} | {r['nombre']} | "
        f"{'SLEP Santa Rosa' if r['dependencia'] == 'slep' else 'Particular subvencionado'} | "
        f"{'Básica/media' if r['oferta'] == 'basica_media' else 'Educación especial'} | "
        f"{r['matricula_total']} | {r['matricula_basica_media']} |"
    )
lines.extend([
    "",
    "La matrícula total incluye parvularia cuando el establecimiento ofrece ese nivel. La columna básica/media separa únicamente la matrícula de esos niveles. Educación especial requiere una comparación propia; no se le asigna ausencia de SIMCE como mal resultado.",
    "",
    "Fuente: [Directorio Oficial de Establecimientos Educacionales, Mineduc](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/). Archivo y diccionario originales en `datos/originales/`.",
])
reports = ROOT / "informes"
reports.mkdir(exist_ok=True)
(reports / "Universo_2025.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

rbds = {r["rbd"] for r in universe}
pas = []
for anio in (2022, 2023, 2024, 2025):
    sheet = load_workbook(ORIG / f"pas_{anio}.xlsx", read_only=True, data_only=True).active
    rows = sheet.values
    columns = next(rows)
    for line, values in enumerate(rows, 2):
        raw = dict(zip(columns, values))
        try:
            rbd = int(raw["EE_RBD"])
        except (TypeError, ValueError):
            continue
        if rbd not in rbds:
            continue
        pas.append({
            "archivo_anio": anio,
            "fila_excel": line,
            "pa_id": raw["PA_ID"],
            "rbd": rbd,
            "nombre_fuente": raw["EE_NOMBRE"],
            "comuna_fuente": raw["EE_NOM_COM"],
            "dependencia_fuente": raw["EE_DEPE"],
            "anio_ingreso": raw["AGNO_INGRESO"],
            "fecha_ingreso_aaaammdd": raw["PA_FEC_ING"],
            "anio_termino": raw["AGNO_TERMINO"],
            "fecha_termino_aaaammdd": raw["PA_FEC_TERMINO"],
            "actividad": raw["ACTIVIDAD"],
            "programa": raw["PROGRAMA"],
            "estado": raw["PA_ESTADO"],
            "instancia": raw["PA_INSTANCIA"],
            "amonestacion_primera": raw["SANCION_AMONESTACION_PRIMERA"],
            "multa_primera": raw["SANCION_MULTA_PRIMERA"],
            "reintegro_primera": raw["SANCION_REINTEGRO_PRIMERA"],
            "monto_multa_primera": raw["MONTO_MULTA_PRIMERA"],
            "monto_reintegro_primera": raw["MONTO_REINTEGRO_PRIMERA"],
            "multa_segunda": raw["SANCION_MULTA_SEGUNDA"],
            "reintegro_segunda": raw["SANCION_REINTEGRO_SEGUNDA"],
            "monto_multa_segunda": raw["MONTO_MULTA_SEGUNDA"],
            "monto_reintegro_segunda": raw["MONTO_REINTEGRO_SEGUNDA"],
            "reclamacion": raw["PA_TIENE_RECLAMACION"],
            "resolucion_termino": raw["N_REX_TERMINO"],
            "resolucion_reclamacion": raw["N_REX_RECLAMACION"],
        })

ids = [p["pa_id"] for p in pas]
if len(ids) != len(set(ids)):
    raise ValueError("Hay PA_ID repetidos entre archivos; revisar antes de contar procesos")
(OUT / "procesos_supereduc_la_cisterna_2022_2025.json").write_text(
    json.dumps(pas, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8"
)

print("Universo", Counter((r["anio"], r["dependencia"], r["oferta"]) for r in universe))
print("Procesos", Counter(p["archivo_anio"] for p in pas))
print("Estados", Counter(p["estado"] for p in pas))
print("Multas primera", sum(p["multa_primera"] == 1 for p in pas))
print("Reintegros primera", sum(p["reintegro_primera"] == 1 for p in pas))

# Las bases SIMCE descargadas por año empaquetan un RAR por grado. Se lee
# únicamente el CSV por RBD y se conserva su versión y fecha de base.
simce = []
for anio in (2023, 2024, 2025):
    outer = ORIG / f"agencia_simce_{anio}.rar"
    inner_names = subprocess.check_output(["tar", "-tf", str(outer)]).decode().splitlines()
    for inner_name in inner_names:
        inner_bytes = subprocess.check_output(["tar", "-xOf", str(outer), inner_name])
        with tempfile.NamedTemporaryFile(suffix=".rar") as tmp:
            tmp.write(inner_bytes)
            tmp.flush()
            members = subprocess.check_output(["tar", "-tf", tmp.name]).decode().splitlines()
            member = next(n for n in members if "_rbd_" in n and n.endswith(".csv"))
            raw_csv = subprocess.check_output(["tar", "-xOf", tmp.name, member])
        decoded = raw_csv.decode("utf-8-sig", errors="replace")
        if decoded.count("\ufffd"):
            decoded = raw_csv.decode("latin1")
        for row in csv.DictReader(io.StringIO(decoded), delimiter=";"):
            try:
                rbd = int(row["rbd"])
            except (TypeError, ValueError):
                continue
            if rbd not in rbds:
                continue
            measures = {
                key: value for key, value in row.items()
                if key.startswith(("nalu_", "prom_", "dif_", "sigdif_", "marca_"))
            }
            simce.append({
                "anio": anio,
                "rbd": rbd,
                "grado": row["grado"],
                "nombre_fuente": row["nom_rbd"],
                "grupo_socioeconomico_codigo": row.get("cod_grupo"),
                "version_base": row.get("codigo_bbdd"),
                "fecha_base_aaaammdd": row.get("fecha_bbdd"),
                "archivo_interno": inner_name,
                "medidas_originales": measures,
            })
assert len({(r["anio"], r["rbd"], r["grado"]) for r in simce}) == len(simce)
(OUT / "simce_la_cisterna_2023_2025.json").write_text(
    json.dumps(simce, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("SIMCE por año y grado", Counter((r["anio"], r["grado"]) for r in simce))

idps = []
for anio in (2023, 2024, 2025):
    outer = ORIG / f"agencia_idps_{anio}.rar"
    inner_names = subprocess.check_output(["tar", "-tf", str(outer)]).decode().splitlines()
    for inner_name in inner_names:
        inner_bytes = subprocess.check_output(["tar", "-xOf", str(outer), inner_name])
        with tempfile.NamedTemporaryFile(suffix=".rar") as tmp:
            tmp.write(inner_bytes)
            tmp.flush()
            members = subprocess.check_output(["tar", "-tf", tmp.name]).decode().splitlines()
            member = next(n for n in members if n.lower().endswith(("_rbd_final.csv", "_rbd_preliminar.csv")))
            raw_csv = subprocess.check_output(["tar", "-xOf", tmp.name, member])
        decoded = raw_csv.decode("utf-8-sig", errors="replace")
        if decoded.count("\ufffd"):
            decoded = raw_csv.decode("latin1")
        grade_match = re.search(r"idps(2m|4b|6b|8b)", member, re.IGNORECASE)
        if not grade_match:
            raise ValueError(f"Grado IDPS desconocido: {member}")
        grade = grade_match.group(1).lower()
        for row in csv.DictReader(io.StringIO(decoded), delimiter=";"):
            try:
                rbd = int(row["rbd"])
            except (TypeError, ValueError):
                continue
            if rbd not in rbds:
                continue
            code = str(row.get("ind") or row.get("id_indicador") or "")
            indicator = {
                "AM": "Autoestima académica y motivación escolar",
                "CC": "Clima de convivencia escolar",
                "PF": "Participación y formación ciudadana",
                "HV": "Hábitos de vida saludable",
                "1": "Autoestima académica y motivación escolar",
                "2": "Clima de convivencia escolar",
                "3": "Participación y formación ciudadana",
                "4": "Hábitos de vida saludable",
            }.get(code)
            if not indicator:
                raise ValueError(f"Código IDPS desconocido: {code}")
            idps.append({
                "anio": anio,
                "rbd": rbd,
                "grado": grade,
                "indicador_codigo_original": code,
                "indicador": indicator,
                "promedio_original": row.get("prom"),
                "diferencia_original": row.get("dif"),
                "significancia_original": row.get("sigdif"),
                "grupo_socioeconomico_codigo": row.get("cod_grupo"),
                "version_base": row.get("codigo_bbdd") or row.get("codigo_bdd"),
                "fecha_base_aaaammdd": row.get("fecha_bbdd"),
                "archivo_interno": inner_name,
                "archivo_csv": member,
            })
assert len({(r["anio"], r["rbd"], r["grado"], r["indicador_codigo_original"]) for r in idps}) == len(idps)
(OUT / "idps_la_cisterna_2023_2025.json").write_text(
    json.dumps(idps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("IDPS por año y grado", Counter((r["anio"], r["grado"]) for r in idps))
