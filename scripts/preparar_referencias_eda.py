"""Recuperación local, sin descargar ni modificar los archivos de origen."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT.parent / 'BI' / ROOT.name
CLASS = ROOT.parent / 'BI' / 'Class'
pairs = {
    OLD/'BI-DatosProyecto/Directorio/Directorio-oficial-EE-2022/20220914_Directorio_Oficial_EE_2022_20220430_WEB.csv': ROOT/'datos/originales/directorio_2022.csv',
    OLD/'BI-DatosProyecto/Directorio/Directorio-Oficial-EE-2023-1/20230912_Directorio_Oficial_EE_2023_20230430_WEB.csv': ROOT/'datos/originales/directorio_2023.csv',
    OLD/'datos/intermedios/pme_2024/20250131_Implementación_PME_2024_20250116.xlsx': ROOT/'datos/originales/pme_implementacion_2024.xlsx',
    OLD/'datos/intermedios/pme_2024/ER Implementación PME 2024.pdf': ROOT/'datos/originales/pme_diccionario_2024.pdf',
    OLD/'GROUP_03_W1/report/GROUP_03_W1_Report.pdf': ROOT/'informes/referencias/W1_con_reflexiones_25-09-2026.pdf',
    CLASS/'Calendarization_2026_Third_Term_Business_Intelligence_IIB423T.docx': ROOT/'informes/referencias/Calendarization_2026_Third_Term_Business_Intelligence_IIB423T.docx',
    CLASS/'03_EDA_after_Data_Validation.pdf': ROOT/'informes/referencias/03_EDA_after_Data_Validation.pdf',
}
records = []
for src, dst in pairs.items():
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    fingerprint = hashlib.sha256(src.read_bytes()).hexdigest()
    if not dst.exists():
        shutil.copy2(src, dst)
    if hashlib.sha256(dst.read_bytes()).hexdigest() != fingerprint:
        raise ValueError(f'Copia distinta: {dst}')
    records.append({'origen_local': str(src), 'archivo': str(dst.relative_to(ROOT)),
                    'sha256': fingerprint, 'bytes': dst.stat().st_size,
                    'fecha_recuperacion': '2026-09-28', 'accion': 'Copia local sin modificar fuente'})
(ROOT/'datos/manifiesto_recuperacion_local.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
print(f'{len(records)} fuentes recuperadas y verificadas por SHA-256')
