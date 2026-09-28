"""Integra órdenes públicas de ChileCompra sin confundir orden con pago.

Requiere los ocho archivos .7z oficiales en data/originales/chilecompra y 7z
en PATH. La llave de una orden es codigoOC, aunque los CSV tengan varias filas
por ítem o por combinación ítem-cotización.
"""
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
ARCHIVES = ROOT / "data/originales/chilecompra"
OUTPUT = ROOT / "data/procesados/la_cisterna"

BUYERS = {
    2022: ("municipal", "100488"),
    2023: ("municipal", "100488"),
    2024: ("municipal", "100488"),
    2025: ("slep", "1890640"),
}
SCHOOLS = {
    9693: (r"LICEO (?:POLITECNICO )?CIENCIA Y TECNOLOGIA",),
    9699: (r"NACIONES UNIDAS",),
    9700: (r"COLEGIO PALESTINO",),
    9701: (r"OLOF PALME",),
    9703: (r"ESPERANZA JOVEN",),
    9706: (r"OSCAR ENCALADA",),
    9722: (r"PORTAL DE LA CISTERNA",),
    9730: (r"\bANTU\b",),
}
OTHER_COMMUNES = ("LO ESPEJO", "PEDRO AGUIRRE CERDA", "SAN RAMON", "SAN MIGUEL")
TEXT_FIELDS = ("NombreOC", "DescripcionOC", "NombreItem", "DescripcionItem",
               "NombreCotizacion", "DescripcionCotizacion", "DescripcionProducto")
FIELDS = ("anio", "codigo_oc", "comprador", "unidad_compra", "fecha_envio", "nombre_oc",
          "descripcion_oc", "estado_oc", "procedencia_oc", "trato_directo", "moneda_oc",
          "monto_total_oc_clp", "monto_oc_vigente_clp", "rbd_asignado", "vinculo_rbd",
          "archivo_fuente")


def normalize(value):
    value = unicodedata.normalize("NFD", str(value or "").upper())
    return "".join(c for c in value if unicodedata.category(c) != "Mn")


def amount(value):
    if not value:
        return None
    try:
        return Decimal(value.replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError(f"Monto inválido {value!r}") from exc


def archive_members(path):
    output = subprocess.check_output(["7z", "l", "-slt", str(path)], text=True)
    return [line[7:] for line in output.splitlines() if line.startswith("Path = ")
            and line.lower().endswith(".csv")]


def rows_from_archive(path):
    for member in archive_members(path):
        proc = subprocess.Popen(["7z", "e", "-so", str(path), member], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        with io.TextIOWrapper(proc.stdout, encoding="latin1", newline="") as stream:
            for row in csv.DictReader(stream, delimiter=";"):
                yield member, row
        if proc.wait() != 0:
            raise RuntimeError(f"No se pudo leer {path.name}:{member}: {proc.stderr.read()!r}")


def matched_schools(text):
    found = set()
    for rbd, names in SCHOOLS.items():
        if re.search(r"\bRBD\s*[:Nº°#.-]*\s*" + str(rbd) + r"\b", text):
            found.add(rbd)
        if any(re.search(pattern, text) for pattern in names):
            found.add(rbd)
    return found


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUTPUT / "manifiesto_chilecompra.json"
    known_hashes = {}
    if manifest_path.exists():
        known_hashes = {entry["archivo"]: entry["sha256"]
                        for entry in json.loads(manifest_path.read_text(encoding="utf-8"))}
    selected = []
    candidates = []
    coverage = []
    manifest = []
    audit = []
    for year, (buyer, code) in BUYERS.items():
        all_orders = {}
        for half in ("Sem1", "Sem2"):
            path = ARCHIVES / f"{buyer}_{year}_{half}.7z"
            if not path.is_file():
                raise FileNotFoundError(path)
            members = archive_members(path)
            fingerprint = hashlib.sha256(path.read_bytes()).hexdigest()
            if path.name in known_hashes and known_hashes[path.name] != fingerprint:
                raise ValueError(f"Archivo ChileCompra cambiado respecto del manifiesto: {path.name}")
            manifest.append({"archivo": path.name, "url": f"https://chc-oc-files.mercadopublico.cl/entcode/{year}/{half}/{code}.7z",
                             "sha256": fingerprint, "miembros": members})
            for member, row in rows_from_archive(path):
                if row.get("entCode") != code:
                    raise ValueError(f"Código comprador inesperado: {path.name} {row.get('entCode')}")
                oc = row.get("codigoOC", "").strip()
                if not oc:
                    raise ValueError(f"Orden sin código en {path.name}:{member}")
                item = all_orders.setdefault(oc, {"row": row, "texts": set(), "source": set(), "raw_rows": 0})
                item["raw_rows"] += 1
                first = item["row"]
                for field in ("MontoTotalOC", "MonedaOC", "ProcedenciaOC", "UnidadCompra", "EstadoOC"):
                    if first.get(field) != row.get(field):
                        raise ValueError(f"Valor inconsistente en {oc}:{field}")
                item["texts"].add(" ".join(row.get(field, "") for field in TEXT_FIELDS))
                item["source"].add(path.name + ":" + member)
        counts = Counter()
        sums = defaultdict(Decimal)
        for oc, item in sorted(all_orders.items()):
            row = item["row"]
            unit = normalize(row.get("UnidadCompra"))
            text = normalize(" ".join(item["texts"]))
            matches = matched_schools(text)
            other_commune = any(name in text for name in OTHER_COMMUNES)
            if buyer == "municipal":
                in_scope = unit == "EDUCACION"
            else:
                in_scope = bool(matches) and len(matches) == 1 and not other_commune
            counts["oc_comprador"] += 1
            if not in_scope:
                if matches:
                    candidates.append({"anio": year, "codigo_oc": oc, "comprador": buyer,
                                       "unidad_compra": row.get("UnidadCompra"),
                                       "rbd_mencionados": " | ".join(map(str, sorted(matches))),
                                       "otra_comuna_mencionada": int(other_commune),
                                       "nombre_oc": row.get("NombreOC"),
                                       "descripcion_oc": row.get("DescripcionOC"),
                                       "motivo_pendiente": "unidad_municipal_fuera_educacion" if buyer == "municipal"
                                       else "slep_multicomuna_o_multi_rbd",
                                       "archivo_fuente": " | ".join(sorted(item["source"]))})
                if buyer == "slep" and matches:
                    counts["oc_mencion_escuela_sin_atribucion"] += 1
                continue
            counts["oc_seleccionadas"] += 1
            counts["filas_originales_seleccionadas"] += item["raw_rows"]
            rbd = next(iter(matches)) if len(matches) == 1 else None
            if rbd:
                counts["oc_rbd_unico"] += 1
            else:
                counts["oc_sin_rbd_unico"] += 1
            direct = normalize(row.get("ProcedenciaOC")) == "TRATO DIRECTO"
            counts["oc_trato_directo"] += int(direct)
            state = normalize(row.get("EstadoOC"))
            current = state in ("ACEPTADA", "RECEPCION CONFORME")
            counts["oc_estado_aceptado_o_recepcion"] += int(current)
            moneda = row.get("MonedaOC")
            total = amount(row.get("MontoTotalOC")) if moneda == "CLP" else None
            if total is not None:
                total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if current and total is not None:
                sums["monto_oc_vigente_clp"] += total
                sums["suma_incorrecta_por_fila_clp"] += total * item["raw_rows"]
                if rbd:
                    sums["monto_oc_rbd_unico_clp"] += total
            elif current and total is None:
                counts["oc_vigente_moneda_no_clp"] += 1
            selected.append({
                "anio": year, "codigo_oc": oc, "comprador": buyer,
                "unidad_compra": row.get("UnidadCompra"), "fecha_envio": row.get("FechaEnvioOC"),
                "nombre_oc": row.get("NombreOC"), "descripcion_oc": row.get("DescripcionOC"),
                "estado_oc": row.get("EstadoOC"), "procedencia_oc": row.get("ProcedenciaOC"),
                "trato_directo": int(direct), "moneda_oc": moneda,
                "monto_total_oc_clp": str(total) if total is not None else "",
                "monto_oc_vigente_clp": str(total) if current and total is not None else "",
                "rbd_asignado": rbd or "",
                "vinculo_rbd": "nombre_o_rbd_unico" if rbd else "unidad_educacion_sin_rbd_unico",
                "archivo_fuente": " | ".join(sorted(item["source"])),
            })
        audit.append({"anio": year, "comprador": buyer,
                      "filas_originales_comprador": sum(item["raw_rows"] for item in all_orders.values()),
                      "oc_unicas_comprador": len(all_orders),
                      "filas_originales_seleccionadas": counts["filas_originales_seleccionadas"],
                      "oc_unicas_seleccionadas": counts["oc_seleccionadas"],
                      "repeticiones_por_item_cotizacion": counts["filas_originales_seleccionadas"] - counts["oc_seleccionadas"],
                      "suma_incorrecta_por_fila_clp": str(sums["suma_incorrecta_por_fila_clp"]),
                      "suma_correcta_por_oc_clp": str(sums["monto_oc_vigente_clp"]),
                      "regla": "Mismo filtro de estado y moneda; total OC contado una vez por codigoOC"})
        coverage.append({"anio": year, "comprador": buyer, **{k: counts[k] for k in
                         ("oc_comprador", "oc_seleccionadas", "oc_rbd_unico", "oc_sin_rbd_unico",
                          "oc_mencion_escuela_sin_atribucion", "oc_trato_directo",
                          "oc_estado_aceptado_o_recepcion", "oc_vigente_moneda_no_clp")},
                         **{k: str(sums[k]) for k in ("monto_oc_vigente_clp", "monto_oc_rbd_unico_clp")}})
    if len({r["codigo_oc"] for r in selected}) != len(selected):
        raise ValueError("Código OC duplicado en selección")
    write_csv(OUTPUT / "oc_escuelas_publicas.csv", selected, FIELDS)
    write_csv(OUTPUT / "oc_candidatas_revision.csv", candidates,
              ("anio", "codigo_oc", "comprador", "unidad_compra", "rbd_mencionados",
               "otra_comuna_mencionada", "nombre_oc", "descripcion_oc", "motivo_pendiente", "archivo_fuente"))
    write_csv(OUTPUT / "oc_cobertura_anual.csv", coverage, list(coverage[0]))
    write_csv(OUTPUT / "oc_limpieza_antes_despues.csv", audit, list(audit[0]))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return coverage


if __name__ == "__main__":
    for entry in run():
        print(entry)
