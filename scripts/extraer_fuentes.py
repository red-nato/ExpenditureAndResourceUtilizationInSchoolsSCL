"""Extracción sin red de anexos CGR y bases Mineduc. Conserva la fila y página originales."""
from pathlib import Path
import json
import pandas as pd
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'datos/originales'
INTER = ROOT / 'datos/intermedios'

def main():
    cache = INTER / 'tablas_cgr.json'
    if not cache.exists():
        result = {}
        with pdfplumber.open(RAW / 'cgr_melipeuco_43_2024.pdf') as doc:
            # No se extrae el anexo con información de estudiantes.
            for anexo, pages in {'compras': range(29,31), 'sin_comodato': range(31,37),
                                  'no_habidos': range(39,64), 'con_comodato': range(63,90)}.items():
                result[anexo] = []
                for page in pages:
                    for index, table in enumerate(doc.pages[page-1].extract_tables()):
                        # Página 63 comparte el cierre del anexo 4 y el inicio del 5.
                        if page == 63 and ((anexo == 'no_habidos' and index != 0) or
                                           (anexo == 'con_comodato' and index == 0)):
                            continue
                        result[anexo].append({'pagina_pdf':page,'filas':table})
                print(anexo, len(result[anexo]), flush=True)
        cache.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    p = INTER/'pme_2024.pkl'
    if not p.exists():
        df = pd.read_excel(next((INTER/'pme_2024').glob('*.xlsx')))
        df.to_pickle(p)
        print('PME',df.shape,flush=True)

if __name__ == '__main__':
    main()
