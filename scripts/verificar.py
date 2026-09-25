"""Comprobaciones de conservación, procedencia y uniones; no pruebas triviales de funciones."""
from pathlib import Path
import pandas as pd
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'datos/procesados'
checks=[]
def check(label,condition):
    checks.append({'control':label,'resultado':'OK' if condition else 'FALLA'})
    if not condition:raise AssertionError(label)
for s in json.loads((ROOT/'datos/fuentes.json').read_text()):
    check('SHA256: '+s['id'],hashlib.sha256((ROOT/s['archivo']).read_bytes()).hexdigest()==s['sha256'])
a=pd.read_csv(P/'cgr_compras_lotes.csv');n=pd.read_csv(P/'cgr_no_habidos.csv');c=pd.read_csv(P/'cgr_con_comodato.csv')
check('Anexo 1: 29 partidas, 776 unidades',len(a)==29 and a.cantidad.sum()==776)
check('Diferencia de $1 preservada',a.valor_clp.sum()==176164030)
check('Anexo 4: 625 filas y $136.000.454',len(n[n.observacion.eq('10.a')])==625 and n.loc[n.observacion.eq('10.a'),'valor_clp'].sum()==136000454)
check('10.a + 10.b + 10.c = 628 y $136.405.378',len(n)==628 and n.valor_clp.sum()==136405378)
check('Anexo 5: 600 filas, $123.816.323',len(c)==600 and c.valor_clp.sum()==123816323)
check('IDs de filas únicos; no se suprimen unidades sin serie',not n.id_fila.duplicated().any())
b=pd.read_csv(P/'cgr_limites_por_dependencia.csv')
check('Límites factibles por dependencia',b.no_habidos_min.le(b.no_habidos_max).all() and b.no_habidos_max.le(b.adquiridos).all())
check('Asignados + no asignados conservan 628',b.no_habidos_min.sum()+18==628)
o=pd.read_csv(P/'cgr_interseccion_comodato_no_habidos.csv')
check('476 coincidencias únicas serie+factura',len(o)==476 and o.clave_serie.nunique()==476)
p=pd.read_csv(P/'pme_panel_establecimientos_2024.csv')
x=pd.read_csv(P/'pme_acciones_nacional_2024.csv')
check('129726 acciones / 8240 escuelas',len(x)==129726 and len(p)==8240)
check('Unión 1:1 no multiplica escuelas',p.RBD.nunique()==len(p))
check('Agregación preserva el total declarado',x.ESTIM_TOTAL.sum()==p.estim_total.sum()==1713979868012)
check('No confundir indicador MATRICULA con conteo MAT_TOTAL',p.MAT_TOTAL.max()>1)
check('Todos los RBD PME enlazan con Directorio 2024',p['_merge'].eq('both').all())
check('Ocho públicos La Cisterna y seis Melipeuco',len(p[p.NOM_COM_RBD.eq('LA CISTERNA')&p.COD_DEPE.isin([1,2,6])])==8 and len(p[p.NOM_COM_RBD.eq('MELIPEUCO')&p.COD_DEPE.isin([1,2,6])])==6)
check('Rangos de avance válidos',p.avance_min.le(p.avance_max).all() and p.avance_max.le(100).all())
pd.DataFrame(checks).to_csv(P/'verificaciones.csv',index=False)
print(f'{len(checks)} controles de integridad y procedencia aprobados.')
