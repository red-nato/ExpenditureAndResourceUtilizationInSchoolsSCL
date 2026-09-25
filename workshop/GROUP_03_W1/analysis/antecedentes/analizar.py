"""EDA reproducible, sin red. Fuentes CGR y Mineduc; ver README para reproducir."""
from pathlib import Path
import json, re, unicodedata, os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/eda_colegios_mpl')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'datos/procesados'
FIG = ROOT/'informes/graficos'
INTER = ROOT/'datos/intermedios'
for p in [OUT, FIG]: p.mkdir(parents=True, exist_ok=True)
sns.set_theme(style='whitegrid', palette=['#156082','#df7634','#438e79','#a25577'])
plt.rcParams.update({'figure.dpi':130, 'savefig.dpi':180, 'font.size':10,
                     'axes.spines.top':False,'axes.spines.right':False})

def save_csv(df, name):
    df.to_csv(OUT/f'{name}.csv', index=False, encoding='utf-8-sig')

def money(s):
    return int(re.sub(r'[^0-9-]', '', str(s)))

def plain(s):
    return ' '.join(str(s).split()) if s is not None else None

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(s).upper()) if not unicodedata.combining(c)).strip()

def school(s):
    s=norm(s).replace('ESCUELA ','').replace(' (*)','')
    return {'VOLCAN LLAIMA':'Volcán Llaima', 'LICEO LOS ANDES':'Los Andes',
            'CAREN':'Carén','CUMCUMLLAQUE':'Cumcumllaque','FUNDO MOLULCO':'Fundo Molulco',
            'MOLULCO':'Molulco','DEM':'DEM','DIFERENTES ESTABLECIMIENTOS':'Sin distribución por escuela'}[s]

def family(s):
    t=norm(s)
    for token,label in [('P11','Lenovo P11 + teclado/lápiz'),('MEDIAPAD','Huawei T3'),('MLAB','Mlab 7'),
                        ('TAB M8','Lenovo M8'),('T505','Samsung A7'),('IPAD','iPad Pro'),
                        ('ASUS','Asus portátil'),('DELL','Dell portátil'),('IMPRESORA','Impresora Epson'),
                        ('AIO LENOVO','Lenovo AIO'),('RYZEN','HP AIO Ryzen'),('HP AIO 20','HP AIO i3')]:
        if token in t:return label
    if 'GALAXY' in t:return 'Samsung A8/T295'
    raise ValueError(s)

def extract_table(j, key):
    records=[]
    for ti,t in enumerate(j[key]):
        previous=None
        for ri,row in enumerate(t['filas'][1:],2):
            if row[0] is None or norm(row[0]) in ['TOTAL','TOTALES']:continue
            r=[plain(s) for s in row]
            if key=='compras' and r[1] is None:
                assert previous and previous[0]==r[0], 'Relleno sólo dentro de misma celda combinada'
                r[1:5]=previous[1:5]
            previous=r.copy()
            records.append(r+[t['pagina_pdf'],ti+1,ri])
    common=['dependencia_original','decreto','fecha_decreto','factura','fecha_factura','modelo_original']
    if key=='compras':cols=common+['cantidad','valor_clp']
    elif key=='sin_comodato':cols=['numero_anexo','dependencia_original','decreto','fecha_decreto','factura','fecha_factura','tipo','comodato','modelo_original']
    else:cols=common+['serie_original','valor_clp']
    d=pd.DataFrame(records,columns=cols+['pagina_pdf','tabla','fila_tabla'])
    d['id_fila']=[f'{key}_{p}_{t}_{r}' for p,t,r in zip(d.pagina_pdf,d.tabla,d.fila_tabla)]
    d['dependencia']=d.dependencia_original.map(school)
    d['familia']=d.modelo_original.map(family)
    d['rbd']=d.dependencia.map({'Los Andes':6007,'Molulco':6009,'Fundo Molulco':6011,'Cumcumllaque':6012,'Carén':6017,'Volcán Llaima':19927}).astype('Int64')
    for col in ['fecha_decreto','fecha_factura']:
        d[col]=pd.to_datetime(d[col],format='%d-%m-%Y',errors='raise')
    if 'valor_clp' in d:d['valor_clp']=d.valor_clp.map(money)
    if 'cantidad' in d:d['cantidad']=d.cantidad.map(money)
    if 'serie_original' in d:
        d['serie']=d.serie_original.map(norm).str.replace(r'\s+','',regex=True)
        d.loc[d.serie_original.str.contains('no identificado|no indica',case=False,na=False),'serie']=pd.NA
    return d

def plot_save(name):
    plt.tight_layout()
    plt.savefig(FIG/f'{name}.png',bbox_inches='tight')
    plt.close()

def analyze_case():
    j=json.loads((INTER/'tablas_cgr.json').read_text())
    a=extract_table(j,'compras'); n=extract_table(j,'no_habidos'); c=extract_table(j,'con_comodato'); s=extract_table(j,'sin_comodato')
    assert len(a)==29 and a.cantidad.sum()==776
    # Se conserva diferencia de $1 entre suma de partidas y total impreso.
    assert a.valor_clp.sum()==176164030
    assert len(n)==625 and n.valor_clp.sum()==136000454
    assert len(c)==600 and c.valor_clp.sum()==123816323
    assert len(s)==144
    extras=pd.DataFrame([
        ['Volcán Llaima',19927,'Huawei T3',82367,'10.b',22],
        ['Volcán Llaima',19927,'Huawei T3',82367,'10.b',22],
        ['Molulco',6009,'Impresora Epson',240190,'10.c',22]],
        columns=['dependencia','rbd','familia','valor_clp','observacion','pagina_pdf'])
    extras['id_fila']=['tabla3_sin_serie_1','tabla3_sin_serie_2','tabla4_impresora_1']
    n['observacion']='10.a'
    full=pd.concat([n,extras],ignore_index=True)
    assert len(full)==628 and full.valor_clp.sum()==136405378
    a['precio_unitario_clp']=a.valor_clp/a.cantidad
    a['dias_factura_decreto']=(a.fecha_decreto-a.fecha_factura).dt.days
    # La familia agrupa descripciones para análisis, sin afirmar equivalencia comercial exacta.
    a['anio']=a.fecha_decreto.dt.year
    a['clave_lote']=a.decreto+'|'+a.factura+'|'+a.familia
    n['clave_lote']=n.decreto+'|'+n.factura+'|'+n.familia
    # La comparación de anexos es por serie exacta y factura; no hay correcciones difusas.
    cn=c[c.serie.notna()].copy()
    cn['clave_serie']=cn.factura+'|'+cn.serie
    nn=n[n.serie.notna()].copy()
    nn['clave_serie']=nn.factura+'|'+nn.serie
    intersection=sorted(set(cn.clave_serie)&set(nn.clave_serie))
    overlap=cn[cn.clave_serie.isin(intersection)].copy()
    dup_n=nn[nn.duplicated('clave_serie',keep=False)]
    dup_c=cn[cn.duplicated('clave_serie',keep=False)]
    # Se conservan filas repetidas sin serie: cada fila representa un equipo en el anexo.
    by_school=a.groupby('dependencia').agg(adquiridos=('cantidad','sum'),compra_clp=('valor_clp','sum')).reset_index()
    nh=full.groupby('dependencia').agg(no_habidos_identificados=('id_fila','size'),valor_no_habido_clp=('valor_clp','sum')).reset_index()
    by_school=by_school.merge(nh,on='dependencia',how='outer',validate='1:1')
    # La factura 13981 distribuye unidades entre 7 destinos; anexo 4 deja parte sin destino.
    unallocated=n[n.dependencia=='Sin distribución por escuela']
    unknown_lots=unallocated.groupby('clave_lote').size()
    bounds=[]
    for dep,g in a.groupby('dependencia'):
        known=int((full.dependencia==dep).sum())
        upper=known
        for key, count in unknown_lots.items():
            capacity=int(g.loc[g.clave_lote==key,'cantidad'].sum())
            assigned=int(((n.clave_lote==key)&(n.dependencia==dep)).sum())
            upper+=min(int(count),max(0,capacity-assigned))
        bounds.append([dep,known,upper,int(g.cantidad.sum())])
    bounds=pd.DataFrame(bounds,columns=['dependencia','no_habidos_min','no_habidos_max','adquiridos'])
    bounds['tasa_min']=bounds.no_habidos_min/bounds.adquiridos
    bounds['tasa_max']=bounds.no_habidos_max/bounds.adquiridos
    by_model=a.groupby('familia').agg(adquiridos=('cantidad','sum'),compra_clp=('valor_clp','sum')).join(
        full.groupby('familia').agg(no_habidos=('id_fila','size'),valor_no_habido_clp=('valor_clp','sum'))).fillna({'no_habidos':0,'valor_no_habido_clp':0}).reset_index()
    by_model['tasa_no_habidos']=by_model.no_habidos/by_model.adquiridos
    by_year=a.groupby('anio').agg(lotes=('id_fila','size'),unidades=('cantidad','sum'),valor_clp=('valor_clp','sum')).reset_index()
    invoices=a.groupby(['decreto','factura','fecha_factura','fecha_decreto']).agg(cantidad=('cantidad','sum'),valor_clp=('valor_clp','sum')).reset_index()
    invoices['dias_factura_decreto']=(invoices.fecha_decreto-invoices.fecha_factura).dt.days
    funds=pd.DataFrame([
        ['SEP',500,123193610],['SEP administración central',9,9269085],['FAEP sin año',15,10969600],
        ['FAEP 2020',47,3871260],['FAEP 2019',175,24885874],['Movámonos 2020',30,3974600]],columns=['fondo','cantidad','valor_clp'])
    assert funds.cantidad.sum()==776 and funds.valor_clp.sum()==176164029
    for df,name in [(a,'cgr_compras_lotes'),(full,'cgr_no_habidos'),(c,'cgr_con_comodato'),(s,'cgr_sin_comodato'),
                    (by_school,'cgr_resumen_dependencia'),(bounds,'cgr_limites_por_dependencia'),(by_model,'cgr_resumen_modelo'),
                    (by_year,'cgr_resumen_anio'),(overlap,'cgr_interseccion_comodato_no_habidos'),(funds,'cgr_fuentes_financiamiento'),
                    (invoices,'cgr_documentos_pago'),(dup_n,'cgr_series_repetidas_no_habidos'),(dup_c,'cgr_series_repetidas_comodato')]:save_csv(df,name)
    case={
      'lotes':len(a),'documentos_pago':len(invoices),'unidades':776,'total_publicado':176164029,'suma_partidas':int(a.valor_clp.sum()),
      'no_habidos':628,'valor_no_habidos':136405378,'tasa_unidades':628/776,'tasa_valor':136405378/176164029,
      'serie_ausente_anexo4':int(n.serie.isna().sum()),'series_distintas_anexo4':int(nn.clave_serie.nunique()),
      'filas_series_duplicadas_anexo4':len(dup_n),'filas_series_duplicadas_anexo5':len(dup_c),
      'coincidencias_serie_factura':len(intersection),'valor_filas_coincidentes':int(overlap.valor_clp.sum()),
      'sin_distribucion_escuela':len(unallocated),'valor_sin_distribucion':int(unallocated.valor_clp.sum()),
      'mediana_dias_factura_decreto':float(invoices.dias_factura_decreto.median()),
      'duplicidad_tic_unidades':61,'duplicidad_tic_valor':12415749,
      'bajas_alegadas':333,'restantes_10a':292,
      'cuota_p11_compra':float(by_model.loc[by_model.familia.str.contains('P11'),'compra_clp'].sum()/a.valor_clp.sum()),
      'cuota_p11_no_habidos':float(by_model.loc[by_model.familia.str.contains('P11'),'valor_no_habido_clp'].sum()/full.valor_clp.sum())}
    # Distribución por lote y por unidad: se declara la ponderación y el carácter no independiente.
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    axes[0].hist(a.precio_unitario_clp/1000,bins=12,color='#156082',edgecolor='white')
    axes[0].set(xlabel='Precio unitario del lote (miles de CLP)',ylabel='Lotes (n=29)',title='Mezclar productos produce una cola larga')
    axes[1].hist(a.precio_unitario_clp/1000,bins=12,weights=a.cantidad,color='#df7634',edgecolor='white')
    axes[1].set(xlabel='Precio unitario (miles de CLP)',ylabel='Unidades adquiridas (n=776)',title='La ponderación cambia la lectura')
    plot_save('01_precios_lotes_unidades')
    q=by_model.sort_values('compra_clp')
    fig,ax=plt.subplots(figsize=(10,5.5))
    ax.barh(q.familia,q.compra_clp/1e6,label='Adquirido',color='#bdcdd4')
    ax.barh(q.familia,q.valor_no_habido_clp/1e6,label='No habido / existencia no validada',color='#df7634')
    ax.set(xlabel='Millones de CLP históricos; valoración del informe',title='Dónde se concentra el valor observado')
    ax.legend(fontsize=8);plot_save('02_valor_por_modelo')
    q=bounds.sort_values('tasa_min')
    fig,ax=plt.subplots(figsize=(10,4.3))
    for i,r in enumerate(q.itertuples()):
        ax.plot([r.tasa_min*100,r.tasa_max*100],[i,i],color='#df7634',lw=5)
        ax.scatter([r.tasa_min*100,r.tasa_max*100],[i,i],color='#156082',s=35)
    ax.set(yticks=range(len(q)),yticklabels=[f'{r.dependencia} (n={r.adquiridos})' for r in q.itertuples()],xlabel='% no habido: mínimo y máximo compatible con asignación pendiente',xlim=(-2,103),title='Tasas por destino: no repartir unidades sin respaldo')
    plot_save('03_limites_por_destino')
    fig,ax=plt.subplots(figsize=(9,3.8))
    ax.bar(['Compra documentada','Observación 10.a','10.b + 10.c','Total observado'],[176164029/1e6,136000454/1e6,404924/1e6,136405378/1e6],color=['#156082','#df7634','#a25577','#df7634'])
    ax.set(ylabel='Millones de CLP',title='Conciliación: los 61 casos TIC están incluidos en 10.a')
    plot_save('04_conciliacion_caso')
    return case

def analyze_pme():
    x=pd.read_pickle(INTER/'pme_2024.pkl').copy()
    x['fila_excel']=np.arange(2,len(x)+2)
    original_cols=[c for c in x if c!='fila_excel']
    x['duplicado_exacto_adicional']=x.duplicated(original_cols,keep='first')
    money_cols=[c for c in x if c.startswith('ESTIM_')]
    components=[c for c in money_cols if c!='ESTIM_TOTAL']
    for col in money_cols:x[col]=pd.to_numeric(x[col],errors='raise')
    x['suma_componentes']=x[components].sum(axis=1,min_count=len(components))
    x['diferencia_total_componentes']=x.ESTIM_TOTAL-x.suma_componentes
    x['total_mayor_1000_millones']=x.ESTIM_TOTAL>1e9
    x['monto_negativo']=(x[money_cols]<0).any(axis=1)
    x['completa']=x.NIV_IMPLEM.eq('Implementación completa: 100%')
    bounds={'Implementación completa: 100%':(100,100),'Implementación avanzada: 75% a 99%':(75,99),
            'Implementación adecuada: 50% a 74%':(50,74),'Implementación parcial: 25% a 49%':(25,49),
            'Implementación inicial: 1% a 24%':(1,24),'Implementación no efectuada: 0%':(0,0)}
    assert x.NIV_IMPLEM.isin(bounds).all()
    x['avance_min']=x.NIV_IMPLEM.map(lambda z:bounds[z][0]);x['avance_max']=x.NIV_IMPLEM.map(lambda z:bounds[z][1])
    d=pd.read_csv(next((INTER/'directorio_2024').glob('*.csv')),sep=';',encoding='utf-8-sig',low_memory=False)
    assert not d.RBD.duplicated().any()
    dc=['RBD','NOM_RBD','NOM_COM_RBD','COD_DEPE','RURAL_RBD','ESTADO_ESTAB','MAT_TOTAL','ENS_01']
    save_csv(d[dc],'directorio_2024_seleccion')
    panel=x.groupby('RBD').agg(acciones=('RBD','size'),estim_total=('ESTIM_TOTAL','sum'),estim_sep=('ESTIM_SEP',lambda z:z.sum(min_count=1)),
          pct_completas=('completa','mean'),avance_min=('avance_min','mean'),avance_max=('avance_max','mean'),
          porc_ben=('PORC_BEN','first'),montos_extremos=('total_mayor_1000_millones','sum'),faltantes_sep=('ESTIM_SEP',lambda z:z.isna().sum()),
          duplicados=('duplicado_exacto_adicional','sum'),nombre_pme=('NOM_RBD','first'))
    panel=panel.reset_index().merge(d[dc],on='RBD',how='left',validate='1:1',indicator=True)
    panel['estim_por_alumno']=panel.estim_total/panel.MAT_TOTAL.where(panel.MAT_TOTAL>0)
    panel['elegible']=panel._merge.eq('both')&panel.ESTADO_ESTAB.eq(1)&panel.MAT_TOTAL.gt(0)
    save_csv(panel,'pme_panel_establecimientos_2024')
    keep=['fila_excel','RBD','NOM_RBD','NOM_COM_RBD','COD_DEPE','DIMENSION','NOM_ACTIVIDAD','DESC_ACTIVIDAD','NIV_IMPLEM',*money_cols,
          'duplicado_exacto_adicional','diferencia_total_componentes','total_mayor_1000_millones']
    save_csv(x.loc[x.NOM_COM_RBD.isin(['LA CISTERNA','MELIPEUCO']),keep],'pme_acciones_pilotos_2024')
    save_csv(x.loc[x.total_mayor_1000_millones,keep],'pme_montos_extremos_para_verificar')
    save_csv(x.loc[x.duplicado_exacto_adicional,keep],'pme_duplicados_exactos')
    # Resumen compacto nacional por acción permite rehacer distribuciones sin reabrir Excel.
    save_csv(x[['fila_excel','RBD','COD_DEPE','DIMENSION','ESTIM_TOTAL','ESTIM_SEP','NIV_IMPLEM','duplicado_exacto_adicional','total_mayor_1000_millones']], 'pme_acciones_nacional_2024')

    # Primer contraste W1: magnitud e implementación declarada por dimensión PME.
    dimensiones=x.groupby('DIMENSION',dropna=False).agg(
        acciones=('RBD','size'),escuelas=('RBD','nunique'),
        estimacion_mediana_clp=('ESTIM_TOTAL','median'),
        estimacion_total_clp=('ESTIM_TOTAL','sum'),
        fraccion_completas=('completa','mean')).reset_index()
    save_csv(dimensiones,'pme_resumen_dimensiones_2024')
    dimensiones['porcentaje_completo']=dimensiones.fraccion_completas*100
    fig,ax=plt.subplots(figsize=(9,4.3))
    q=dimensiones.sort_values('porcentaje_completo')
    ax.barh(q.DIMENSION,q.porcentaje_completo,color='#377f70')
    ax.set(xlim=(0,75),xlabel='Acciones declaradas completas (%)',
           title='PME 2024: implementación declarada por dimensión')
    for i,row in enumerate(q.itertuples()):
        ax.text(row.porcentaje_completo+0.7,i,f'{row.porcentaje_completo:.1f}%',va='center',fontsize=9)
    plot_save('10_pme_dimensiones')
    def summarize(z,label):
        return {'escenario':label,'acciones':len(z),'rbd':z.RBD.nunique(),'total_estimado_clp':int(z.ESTIM_TOTAL.sum()),
                'media_accion_clp':z.ESTIM_TOTAL.mean(),'mediana_accion_clp':z.ESTIM_TOTAL.median(),
                'fraccion_completas':z.completa.mean(),'fraccion_monto_en_completas':z.loc[z.completa,'ESTIM_TOTAL'].sum()/z.ESTIM_TOTAL.sum()}
    sens=pd.DataFrame([summarize(x,'Todos los registros'),summarize(x[~x.total_mayor_1000_millones],'Sensibilidad: acción ≤ $1.000 millones'),
                       summarize(x[~x.duplicado_exacto_adicional],'Sensibilidad: sin duplicados exactos adicionales')])
    save_csv(sens,'pme_sensibilidad_montos')
    save_csv(x.groupby('NIV_IMPLEM').agg(acciones=('RBD','size'),estim_total=('ESTIM_TOTAL','sum')).reset_index(),'pme_nivel_implementacion')
    z=panel[panel.elegible].copy()
    vars=['MAT_TOTAL','acciones','estim_total','estim_por_alumno','porc_ben','pct_completas']
    corrs=[]
    for subset,label in [(z,'Todos elegibles'),(z[z.montos_extremos.eq(0)],'Sin escuelas con acción > $1.000 millones')]:
        for i,v in enumerate(vars):
            for w in vars[i+1:]:
                p=subset[[v,w]].dropna()
                corrs.append([label,v,w,len(p),p[v].corr(p[w],method='pearson'),p[v].corr(p[w],method='spearman')])
    corr=pd.DataFrame(corrs,columns=['escenario','variable_1','variable_2','n_pares','pearson','spearman'])
    save_csv(corr,'pme_correlaciones')
    # Comparaciones dentro de dependencia y ruralidad; n explícito. Sin interpretación causal.
    strata=[]
    for keys,g in z.groupby(['COD_DEPE','RURAL_RBD']):
        p=g[['estim_por_alumno','pct_completas']].dropna()
        if len(p)>=30:
            strata.append([*keys,len(p),p.estim_por_alumno.corr(p.pct_completas,method='spearman')])
    save_csv(pd.DataFrame(strata,columns=['dependencia','rural','n','rho_estim_por_alumno_completas']),'pme_correlaciones_estratificadas')
    # Brechas de cobertura sobre el universo oficial activo con matrícula.
    d['en_pme']=d.RBD.isin(x.RBD)
    universe=d[d.ESTADO_ESTAB.eq(1)&d.MAT_TOTAL.gt(0)]
    coverage=universe.groupby('COD_DEPE').agg(establecimientos=('RBD','size'),con_pme=('en_pme','sum')).reset_index()
    coverage['cobertura']=coverage.con_pme/coverage.establecimientos
    save_csv(coverage,'pme_cobertura_dependencia')
    pilot=panel[panel.NOM_COM_RBD.isin(['LA CISTERNA','MELIPEUCO'])].copy()
    save_csv(pilot,'pme_panel_pilotos_2024')
    public_pilot=pilot[pilot.COD_DEPE.isin([1,2,6])].copy()
    fig,ax=plt.subplots(figsize=(10,5.5))
    q=public_pilot[public_pilot.NOM_COM_RBD.eq('LA CISTERNA')].sort_values('avance_min')
    for i,r in enumerate(q.itertuples()):
        ax.plot([r.avance_min,r.avance_max],[i,i],color='#156082',lw=4)
        ax.scatter(r.pct_completas*100,i,color='#df7634',s=40,zorder=3)
    ax.set(yticks=range(len(q)),yticklabels=q.NOM_RBD.str.replace('ESCUELA BAS. ','',regex=False).str.replace('LICEO POLITECNICO ','',regex=False),
           xlabel='Porcentaje; promedio simple entre acciones',xlim=(-2,102),title='La Cisterna: rango de avance y fracción de acciones completas')
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([0],[0],color='#156082',lw=4,label='Límites del avance medio declarado'),
                       Line2D([0],[0],marker='o',color='white',markerfacecolor='#df7634',label='Acciones al 100%')],fontsize=8)
    plot_save('09_pme_rangos_la_cisterna')
    missing=x.isna().sum().rename_axis('variable').reset_index(name='faltantes')
    missing['porcentaje']=missing.faltantes/len(x)*100
    save_csv(missing,'pme_faltantes')
    desc=x.ESTIM_TOTAL.describe(percentiles=[.25,.5,.75,.9,.95,.99,.999]).rename_axis('estadistico').reset_index(name='valor')
    save_csv(desc,'pme_descriptivos_montos')
    pme={'acciones':len(x),'rbd':x.RBD.nunique(),'duplicados_adicionales':int(x.duplicado_exacto_adicional.sum()),
         'faltantes_sep':int(x.ESTIM_SEP.isna().sum()),'negativos':int(x.monto_negativo.sum()),
         'discrepancias_componentes':int(x.diferencia_total_componentes.ne(0).where(x.diferencia_total_componentes.notna(),False).sum()),
         'discrepancias_mayor_1':int(x.diferencia_total_componentes.abs().gt(1).sum()),
         'acciones_extremas':int(x.total_mayor_1000_millones.sum()),'fraccion_total_extremas':float(x.loc[x.total_mayor_1000_millones,'ESTIM_TOTAL'].sum()/x.ESTIM_TOTAL.sum()),
         'acciones_cero':int(x.ESTIM_TOTAL.eq(0).sum()),'total_estimado':int(x.ESTIM_TOTAL.sum()),
         'mediana':float(x.ESTIM_TOTAL.median()),'media':float(x.ESTIM_TOTAL.mean()),'pct_completas':float(x.completa.mean()),
         'sin_directorio':int(panel._merge.eq('left_only').sum()),'escuelas_elegibles':len(z),
         'fecha_invertida':int((pd.to_datetime(x.FECHA_TERMINO)<pd.to_datetime(x.FECHA_INICIO)).sum())}
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    axes[0].hist(x.ESTIM_TOTAL/1e6,bins=60,color='#156082')
    axes[0].set(xlabel='Monto estimado por acción (millones de CLP)',ylabel='Acciones',title='Escala original: dominada por valores extremos')
    positive=np.log10(x.loc[x.ESTIM_TOTAL.gt(0),'ESTIM_TOTAL'])
    axes[1].hist(positive,bins=45,density=True,color='#b4cbd5',label='Histograma')
    sns.kdeplot(positive,ax=axes[1],color='#156082',bw_adjust=1,cut=0,label='Densidad suavizada')
    axes[1].set(xlabel='log10(monto positivo en CLP)',ylabel='Densidad',title=f'Escala logarítmica; {pme["acciones_cero"]:,} ceros aparte')
    axes[1].legend();plot_save('05_pme_histograma_densidad')
    fig,ax=plt.subplots(figsize=(9,5.5))
    labels=['Matrícula','N.º acciones','Estimado total','Estimado/alumno','% beneficiarios','Fracción completas']
    cc=z[vars].corr(method='spearman'); cc.index=labels;cc.columns=labels
    sns.heatmap(cc,annot=True,fmt='.2f',vmin=-1,vmax=1,cmap='vlag',ax=ax)
    ax.set_title(f'Correlaciones Spearman: {len(z):,} establecimientos elegibles')
    plot_save('06_pme_correlaciones')
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    pos=z[z.estim_total.gt(0)]
    axes[0].hexbin(np.log10(pos.MAT_TOTAL),np.log10(pos.estim_total),gridsize=40,mincnt=1,cmap='Blues',bins='log')
    axes[0].set(xlabel='log10(matrícula)',ylabel='log10(monto estimado total)',title='Más tamaño, mayor presupuesto declarado')
    axes[1].hexbin(np.log10(pos.estim_por_alumno),pos.pct_completas*100,gridsize=35,mincnt=1,cmap='Oranges',bins='log')
    axes[1].set(xlabel='log10(estimado por estudiante)',ylabel='% de acciones completas',title='Implementación declarada, no uso comprobado')
    plot_save('07_pme_relaciones')
    fig,ax=plt.subplots(figsize=(9,4.5))
    pp=x[x.ESTIM_TOTAL.gt(0)].copy();pp['log_monto']=np.log10(pp.ESTIM_TOTAL)
    sns.boxplot(data=pp,x='DIMENSION',y='log_monto',showfliers=False,ax=ax,color='#a3c3d1')
    ax.set(xlabel='',ylabel='log10(estimación positiva, CLP)',title='Distribución por dimensión PME; atípicos ocultos sólo en este gráfico')
    plot_save('08_pme_dimensiones')
    return pme

def main():
    result={'caso':analyze_case(),'pme':analyze_pme()}
    (OUT/'resultados.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
