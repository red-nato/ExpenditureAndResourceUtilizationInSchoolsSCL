"""Registra la procedencia y huella SHA-256 de las descargas originales."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "datos" / "originales"

urls = {
    "directorio_2024.rar": "https://datosabiertos.mineduc.cl/wp-content/uploads/2024/11/Directorio-Oficial-EE-2024-.rar",
    "directorio_2025.rar": "https://datosabiertos.mineduc.cl/wp-content/uploads/2025/11/Directorio-Oficial-EE-2025.rar",
    "supereduc_pas_2022.zip": "https://www.supereduc.cl/wp-content/uploads/2026/02/PA_2022.zip",
    "supereduc_pas_2023.zip": "https://www.supereduc.cl/wp-content/uploads/2026/02/PA_2023.zip",
    "supereduc_pas_2024.zip": "https://www.supereduc.cl/wp-content/uploads/2026/02/PA_2024.zip",
    "supereduc_pas_2025.zip": "https://www.supereduc.cl/wp-content/uploads/2026/02/PA-2025.zip",
    "supereduc_pas_diccionario.zip": "https://www.supereduc.cl/wp-content/uploads/2026/02/PA_ER.zip",
    "agencia_simce_2023.rar": "https://informacionestadistica.agenciaeducacion.cl/rest/archivo/obtener?uuid=be3f54a6-c5cb-4dc6-ba1d-4b142d3a817d%3B1.0",
    "agencia_simce_2024.rar": "https://informacionestadistica.agenciaeducacion.cl/rest/archivo/obtener?uuid=077d27a6-56de-4df1-b296-71234b080271%3B1.0",
    "agencia_simce_2025.rar": "https://informacionestadistica.agenciaeducacion.cl/rest/archivo/obtener?uuid=1ba2ac5c-17ff-40d7-8b9a-7c90bcef3cdf%3B1.0",
    "agencia_idps_2023.rar": "https://informacionestadistica.agenciaeducacion.cl/rest/archivo/obtener?uuid=6e5b2b84-cce1-4bf1-8d71-ec42402be1e4%3B1.0",
    "agencia_idps_2024.rar": "https://informacionestadistica.agenciaeducacion.cl/rest/archivo/obtener?uuid=e89a63fb-0e9f-442d-9434-591fa3b8b5c6%3B1.0",
    "agencia_idps_2025.rar": "https://informacionestadistica.agenciaeducacion.cl/rest/archivo/obtener?uuid=a553dd88-2a7a-4232-81ac-73fe39d3629c%3B1.0",
}

sources = []
for name, url in urls.items():
    file = ORIG / name
    if not file.is_file():
        raise FileNotFoundError(file)
    sources.append({
        "archivo": str(file.relative_to(ROOT)),
        "url": url,
        "bytes": file.stat().st_size,
        "sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
        "fecha_revision_local": "2026-09-25",
    })
(ROOT / "datos" / "fuentes.json").write_text(
    json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"{len(sources)} archivos originales registrados")
