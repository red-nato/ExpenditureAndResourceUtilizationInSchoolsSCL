"""Ocho etapas auditables para el censo escolar de La Cisterna.

Load -> Profile -> Explore -> Clean -> Impute -> Transform -> Validate -> Explore again.
Los archivos de entrada permanecen intactos. Este módulo funciona sin red.
"""
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
import csv
import hashlib
import json

SOURCES = {
    "directorio": "universo_la_cisterna_2022_2025.json",
    "pas": "procesos_supereduc_la_cisterna_2022_2025.json",
    "pme": "pme_la_cisterna_2024.csv",
    "simce": "simce_la_cisterna_2023_2025.json",
    "idps": "idps_la_cisterna_2023_2025.json",
}


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def numeric(value):
    if value is None or str(value).strip() == "":
        return None
    try:
        return Decimal(str(value).strip())
    except InvalidOperation as error:
        raise ValueError(f"Valor numérico inválido: {value!r}") from error


def run(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    # LOAD: contar filas de cada extracto sin convertir ausencia a cero.
    manifest_path = input_dir / "manifiesto_extraccion.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest["extractos"]:
            actual = hashlib.sha256((input_dir / entry["archivo"]).read_bytes()).hexdigest()
            if actual != entry["sha256"]:
                raise ValueError(f"Huella alterada: {entry['archivo']}")
    raw = {}
    for name, filename in SOURCES.items():
        path = input_dir / filename
        if name == "pme":
            with path.open(encoding="utf-8-sig", newline="") as handle:
                raw[name] = list(csv.DictReader(handle))
        else:
            raw[name] = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw[name], list):
            raise ValueError(f"{filename} debe contener filas")
    with (output_dir / "oc_escuelas_publicas.csv").open(encoding="utf-8", newline="") as handle:
        oc = list(csv.DictReader(handle))
    stage = [{"etapa": "Load", "control": "Cinco extractos base, órdenes deduplicadas y SHA-256 de manifiestos", "resultado": "; ".join(f"{k}={len(v)}" for k, v in {**raw, "oc_seleccionadas": oc}.items())}]

    # PROFILE: llave natural propuesta, nulos en campos críticos y repetición previa al join.
    key_fields = {"directorio": ("anio", "rbd"), "pas": ("pa_id",), "pme": ("fila_excel",),
                  "simce": ("anio", "rbd", "grado"),
                  "idps": ("anio", "rbd", "grado", "indicador_codigo_original")}
    important = {"directorio": ("dependencia", "matricula_total", "oferta"),
                 "pas": ("archivo_anio", "rbd", "estado", "instancia"),
                 "pme": ("RBD", "ESTIM_TOTAL", "NIV_IMPLEM"),
                 "simce": ("version_base", "medidas_originales"),
                 "idps": ("version_base", "promedio_original")}
    profile = []
    for name, rows in raw.items():
        keys = [tuple(row.get(field) for field in key_fields[name]) for row in rows]
        duplicates = len(keys) - len(set(keys))
        missing = {field: sum(row.get(field) in (None, "") for row in rows) for field in (*key_fields[name], *important[name])}
        profile.append({"fuente": name, "filas": len(rows), "llave_propuesta": " + ".join(key_fields[name]),
                        "llaves_duplicadas": duplicates, "nulos_criticos": json.dumps(missing, ensure_ascii=False)})
    oc_keys = [row["codigo_oc"] for row in oc]
    profile.append({"fuente": "oc_seleccionadas", "filas": len(oc), "llave_propuesta": "codigo_oc",
                    "llaves_duplicadas": len(oc_keys) - len(set(oc_keys)),
                    "nulos_criticos": json.dumps({"codigo_oc": sum(not x for x in oc_keys),
                                                   "rbd_asignado": sum(not row["rbd_asignado"] for row in oc)}, ensure_ascii=False)})
    write_csv(output_dir / "perfil_fuentes.csv", profile, list(profile[0]))
    stage.append({"etapa": "Profile", "control": "Duplicados por llave natural", "resultado": str({r["fuente"]: r["llaves_duplicadas"] for r in profile})})

    # EXPLORE: descripción previa a transformación, sin combinar fuentes.
    raw_years = dict(sorted(Counter(row["anio"] for row in raw["directorio"]).items()))
    raw_pas_years = dict(sorted(Counter(row["archivo_anio"] for row in raw["pas"]).items()))
    stage.append({"etapa": "Explore", "control": "Denominadores preliminares por año", "resultado": f"Directorio={raw_years}; PAS por archivo={raw_pas_years}"})

    # CLEAN: tipos explícitos; conservar los valores originales en las entradas.
    universe = []
    for row in raw["directorio"]:
        clean = dict(row)
        clean["anio"], clean["rbd"], clean["matricula_total"] = int(row["anio"]), int(row["rbd"]), int(row["matricula_total"])
        clean["dependencia"] = str(row["dependencia"]).strip()
        universe.append(clean)
    pas = [{**row, "pa_id": int(row["pa_id"]), "rbd": int(row["rbd"]), "archivo_anio": int(row["archivo_anio"])} for row in raw["pas"]]
    # La base PAS no publica materia/cargos. No inferirlos de actividad, programa o sanción.
    pas_materia = [{"pa_id": r["pa_id"], "rbd": r["rbd"], "archivo_anio": r["archivo_anio"],
                   "actividad": r["actividad"], "programa": r["programa"], "estado": r["estado"],
                   "materia_confirmada": "", "clasificacion_materia": "sin_antecedente_en_base_pas"} for r in pas]
    write_csv(output_dir / "pas_revision_materia.csv", pas_materia, list(pas_materia[0]))
    pme = []
    for row in raw["pme"]:
        clean = dict(row)
        clean["RBD"] = int(row["RBD"])
        clean["fila_excel"] = int(row["fila_excel"])
        clean["estimacion_clp"] = numeric(row["ESTIM_TOTAL"])
        pme.append(clean)
    simce = [{**row, "anio": int(row["anio"]), "rbd": int(row["rbd"]), "grado": str(row["grado"]).lower().strip()} for row in raw["simce"]]
    idps = [{**row, "anio": int(row["anio"]), "rbd": int(row["rbd"]), "grado": str(row["grado"]).lower().strip(),
             "promedio": numeric(row.get("promedio_original"))} for row in raw["idps"]]
    stage.append({"etapa": "Clean", "control": "Normalización conservadora", "resultado": "RBD/año enteros; grados normalizados; montos y promedios decimales; sin descartar filas"})

    # IMPUTE: solo conteos derivados de filas ausentes; puntajes/montos permanecen NA.
    stage.append({"etapa": "Impute", "control": "Política de faltantes", "resultado": "No se imputan montos, puntajes ni pagos. Cero OC vinculadas significa cero coincidencias verificadas, no cero compras."})

    # TRANSFORM: agregar cada fuente a RBD antes de unir; PAS se asocia al censo anual,
    # y se separa el año del archivo del año de ingreso/término.
    by_year = {year: {r["rbd"]: r for r in universe if r["anio"] == year} for year in range(2022, 2026)}
    pas_count = Counter((r["archivo_anio"], r["rbd"]) for r in pas)
    pme_count = Counter(r["RBD"] for r in pme)
    pme_amount = defaultdict(Decimal)
    for row in pme:
        if row["estimacion_clp"] is not None:
            pme_amount[row["RBD"]] += row["estimacion_clp"]
    by_dimension = defaultdict(list)
    for row in pme:
        by_dimension[row["DIMENSION"]].append(row)
    pme_dimensions = []
    for dimension, rows in sorted(by_dimension.items()):
        amounts = sorted(r["estimacion_clp"] for r in rows if r["estimacion_clp"] is not None)
        middle = len(amounts) // 2
        median = (amounts[middle] if len(amounts) % 2 else (amounts[middle - 1] + amounts[middle]) / 2) if amounts else None
        pme_dimensions.append({"dimension": dimension, "acciones": len(rows), "rbd": len({r["RBD"] for r in rows}),
                               "declaradas_completas": sum(r["NIV_IMPLEM"] == "Implementación completa: 100%" for r in rows),
                               "estimacion_cero": sum(r["estimacion_clp"] == 0 for r in rows),
                               "mediana_estimacion_clp": str(median) if median is not None else ""})
    write_csv(output_dir / "pme_dimensiones.csv", pme_dimensions, list(pme_dimensions[0]))
    simce_count = Counter((r["anio"], r["rbd"]) for r in simce)
    idps_count = Counter((r["anio"], r["rbd"]) for r in idps)
    oc_count = Counter((int(r["anio"]), int(r["rbd_asignado"])) for r in oc if r["rbd_asignado"])
    oc_direct = Counter((int(r["anio"]), int(r["rbd_asignado"])) for r in oc
                        if r["rbd_asignado"] and r["trato_directo"] == "1")
    oc_amount = defaultdict(Decimal)
    for r in oc:
        if r["rbd_asignado"] and r["monto_oc_vigente_clp"]:
            oc_amount[int(r["anio"]), int(r["rbd_asignado"])] += numeric(r["monto_oc_vigente_clp"])
    panel = []
    for row in universe:
        year, rbd = row["anio"], row["rbd"]
        pas_n = pas_count[year, rbd]
        pme_n = pme_count[rbd] if year == 2024 else None
        panel.append({"anio": year, "rbd": rbd, "nombre": row["nombre"], "dependencia": row["dependencia"],
                      "oferta": row["oferta"], "matricula_total": row["matricula_total"],
                      "pas_filas_archivo_anual": pas_n, "tiene_pas_publicado": int(pas_n > 0),
                      "pme_acciones_2024": pme_n, "tiene_pme_registro_2024": int(pme_n > 0) if year == 2024 else None,
                      "pme_estimacion_clp_2024": str(pme_amount[rbd]) if pme_n else None,
                      "simce_filas": simce_count[year, rbd] if year >= 2023 else None,
                      "idps_filas": idps_count[year, rbd] if year >= 2023 else None,
                      "oc_rbd_vinculadas": oc_count[year, rbd] if row["dependencia"] in ("municipal_daem", "slep") else None,
                      "oc_trato_directo_rbd_vinculadas": oc_direct[year, rbd] if row["dependencia"] in ("municipal_daem", "slep") else None,
                      "oc_monto_vigente_clp_rbd_vinculado": str(oc_amount[year, rbd]) if (year, rbd) in oc_amount else None})
    write_csv(output_dir / "panel_rbd_anual.csv", panel, list(panel[0]))
    annual = []
    for year in range(2022, 2026):
        for group in ("municipal_daem", "slep", "particular_subvencionado"):
            rows = [r for r in universe if r["anio"] == year and r["dependencia"] == group]
            if rows:
                annual.append({"anio": year, "dependencia": group, "rbd": len(rows),
                               "basica_media": sum(r["oferta"] == "basica_media" for r in rows),
                               "especial": sum(r["oferta"] == "especial" for r in rows),
                               "matricula_total": sum(r["matricula_total"] for r in rows)})
    write_csv(output_dir / "universo_anual.csv", annual, list(annual[0]))
    agency = []
    for year, grade in sorted({(r["anio"], r["grado"]) for r in simce + idps}):
        ss = [r for r in simce if (r["anio"], r["grado"]) == (year, grade)]
        ii = [r for r in idps if (r["anio"], r["grado"]) == (year, grade)]
        with_score = {r["rbd"] for r in ss if any(numeric(value) is not None for key, value in r["medidas_originales"].items() if key.startswith("prom_"))}
        agency.append({"anio": year, "grado": grade, "simce_filas": len(ss),
                       "simce_rbd_con_fila": len({r["rbd"] for r in ss}), "simce_rbd_con_puntaje": len(with_score),
                       "idps_filas": len(ii), "idps_rbd_con_fila": len({r["rbd"] for r in ii}),
                       "idps_rbd_con_promedio": len({r["rbd"] for r in ii if r["promedio"] is not None}),
                       "versiones_simce": "; ".join(sorted({str(r["version_base"]) for r in ss})),
                       "versiones_idps": "; ".join(sorted({str(r["version_base"]) for r in ii}))})
    write_csv(output_dir / "cobertura_agencia_por_grado.csv", agency, list(agency[0]))
    stage.append({"etapa": "Transform", "control": "Agregación previa al cruce", "resultado": f"Panel={len(panel)} RBD-año; OC con RBD único={sum(oc_count.values())}; OC sin RBD único={sum(not r['rbd_asignado'] for r in oc)}"})

    # VALIDATE: llaves, pertenencia por RBD-año, conservación de filas y controles sustantivos.
    def unique(rows, fields):
        values = [tuple(r.get(field) for field in fields) for r in rows]
        return len(values) == len(set(values))

    assert unique(universe, ("anio", "rbd"))
    assert unique(pas, ("pa_id",))
    assert len(pas_materia) == len(pas)
    assert unique(pme, ("fila_excel",))
    assert unique(simce, ("anio", "rbd", "grado"))
    assert unique(idps, ("anio", "rbd", "grado", "indicador_codigo_original"))
    assert unique(oc, ("codigo_oc",))
    assert {r["rbd"] for r in pas} <= {r["rbd"] for r in universe}
    assert {r["RBD"] for r in pme} <= set(by_year[2024])
    assert all(r["rbd"] in by_year[r["anio"]] for r in simce + idps)
    assert len(panel) == len(universe) == sum(r["rbd"] for r in annual)
    assert sum(r["pme_acciones_2024"] or 0 for r in panel) == len(pme)
    assert sum(r["acciones"] for r in pme_dimensions) == len(pme)
    assert sum(r["pas_filas_archivo_anual"] for r in panel) == len(pas)
    assert sum(r["oc_rbd_vinculadas"] or 0 for r in panel) == sum(bool(r["rbd_asignado"]) for r in oc)
    assert all(int(r["rbd_asignado"]) in by_year[int(r["anio"])] for r in oc if r["rbd_asignado"])
    assert {year: len(rows) for year, rows in by_year.items()} == {2022: 60, 2023: 60, 2024: 59, 2025: 59}
    assert len(pas) == 110 and len(pme) == 767 and len(simce) == 236 and len(idps) == 936
    assert all(r["matricula_total"] > 0 and r["oferta"] != "revisar" for r in universe)
    stage.append({"etapa": "Validate", "control": "Conservación y enlace", "resultado": "238 RBD-año; 110 PAS, 767 PME, 236 SIMCE, 936 IDPS; OC deduplicadas por código; sin multiplicación en join"})

    # EXPLORE AGAIN: cifras sobre datos tipados/validados y distinción entre faltante y cero.
    pme_rbd = {r["RBD"] for r in pme}
    pme_public = sum(rbd in pme_rbd for rbd, row in by_year[2024].items() if row["dependencia"] == "municipal_daem")
    pme_private = sum(rbd in pme_rbd for rbd, row in by_year[2024].items() if row["dependencia"] == "particular_subvencionado")
    pas_rbd = {r["rbd"] for r in pas}
    metrics = {
        "universo_anual": {str(y): len(rows) for y, rows in by_year.items()},
        "cambio_censo": {"rbd_solo_2022_2023": sorted((set(by_year[2022]) | set(by_year[2023])) - (set(by_year[2024]) | set(by_year[2025]))),
                         "publicos_daem_2024": 8, "publicos_slep_2025": 8},
        "pas": {"procesos": len(pas), "rbd_distintos": len(pas_rbd), "por_archivo": {str(y): n for y, n in raw_pas_years.items()},
                "multas_primera": sum(r["multa_primera"] == 1 for r in pas),
                "reintegros_primera": sum(r["reintegro_primera"] == 1 for r in pas)},
        "pme": {"acciones": len(pme), "rbd_con_fila": len(pme_rbd), "publicos_con_fila": pme_public,
                "particulares_con_fila": pme_private,
                "declaradas_completas": sum(r["declaradas_completas"] for r in pme_dimensions),
                "estimacion_cero": sum(r["estimacion_cero"] for r in pme_dimensions),
                "estimacion_total_clp": str(sum((r["estimacion_clp"] or Decimal(0)) for r in pme))},
        "agencia": {"simce_filas": len(simce), "idps_filas": len(idps),
                    "simce_rbd_con_puntaje_por_anio_grado": [r for r in agency]},
        "chilecompra": {"oc_seleccionadas": len(oc), "oc_rbd_unico": sum(oc_count.values()),
                         "oc_sin_rbd_unico": sum(not r["rbd_asignado"] for r in oc),
                         "trato_directo_seleccionadas": sum(r["trato_directo"] == "1" for r in oc)},
    }
    (output_dir / "metricas.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stage.append({"etapa": "Explore again", "control": "Lectura final", "resultado": f"PME con fila: públicos {pme_public}/8, particulares {pme_private}/51; no se calcula malgasto"})
    write_csv(output_dir / "controles_etapas.csv", stage, ["etapa", "control", "resultado"])
    return metrics
