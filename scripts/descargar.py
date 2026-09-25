"""Recupera originales faltantes y valida sus hashes contra el manifiesto de esta entrega."""
from pathlib import Path
import hashlib,json,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
sources=json.loads((ROOT/'datos/fuentes.json').read_text())
for source in sources:
    path=ROOT/source['archivo']
    if not path.exists():
        path.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(['curl','-L','--fail','--max-time','180',source['url_descarga'],'-o',str(path)],check=True)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=source['sha256']:
        sys.exit(f'La fuente cambió o está incompleta: {path.name}. Conservar y revisar antes de continuar.')
    print('Verificado:',path.name)
for year in [2021,2024]:
    target=ROOT/f'datos/intermedios/directorio_{year}'
    target.mkdir(parents=True,exist_ok=True)
    subprocess.run(['tar','-xf',str(ROOT/f'datos/originales/directorio_{year}.rar'),'-C',str(target)],check=True)
target=ROOT/'datos/intermedios/pme_2024'
target.mkdir(parents=True,exist_ok=True)
subprocess.run(['tar','-xf',str(ROOT/'datos/originales/pme_implementacion_2024.rar'),'-C',str(target)],check=True)
