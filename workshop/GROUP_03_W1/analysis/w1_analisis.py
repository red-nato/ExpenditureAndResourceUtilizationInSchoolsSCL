"""W1: inspección reproducible de dos preguntas educativas con datos incluidos en data/."""
from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "analysis" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

def read(name):
    return pd.read_csv(DATA / name)

def main():
    compras = read("cgr_compras_lotes.csv")
    observados = read("cgr_no_habidos.csv")
    comodatos = read("cgr_con_comodato.csv")
    acciones = read("pme_acciones_campos_seleccionados_2024.csv")
    directorio = read("directorio_campos_seleccionados_2024.csv")
    piloto = read("pme_cisterna_extracto_2024.csv")

    # Unidades: partida del anexo 1, activo observado, acción PME y RBD.
    assert len(compras) == 29 and int(compras.cantidad.sum()) == 776
    assert len(observados) == 628 and int(observados.valor_clp.sum()) == 136405378
    assert len(comodatos) == 600
    assert len(acciones) == 129726 and acciones.RBD.nunique() == 8240
    assert directorio.RBD.is_unique
    assert len(piloto) == 134 and piloto.RBD.nunique() == 8
    assert set(acciones.RBD).issubset(set(directorio.RBD))

    # A: custodias. El valor impreso CGR difiere en $1 de la suma de filas.
    familias = (observados.groupby("familia", dropna=False)
        .agg(equipos=("id_fila","size"), valor_observado_clp=("valor_clp","sum"))
        .sort_values("valor_observado_clp",ascending=False).reset_index())
    familias.to_csv(OUT/"a_familias_observadas.csv",index=False)
    estados = (observados.groupby("observacion",dropna=False)
        .agg(equipos=("id_fila","size"), valor_observado_clp=("valor_clp","sum"))
        .reset_index())
    estados.to_csv(OUT/"a_tipos_observacion.csv",index=False)

    x = observados.dropna(subset=["serie","factura"])
    y = comodatos.dropna(subset=["serie","factura"])
    # Las claves se comprobaron únicas dentro de cada anexo; no hay unión múltiple.
    assert not x.duplicated(["factura","serie"]).any()
    assert not y.duplicated(["factura","serie"]).any()
    cruce = x.merge(y[["factura","serie"]],on=["factura","serie"],validate="one_to_one")
    assert len(cruce)==476 and int(cruce.valor_clp.sum())==106512158
    cruce[["factura","serie","familia","valor_clp","pagina_pdf"]].to_csv(
        OUT/"a_coincidencias_comodato_observado.csv",index=False)

    fig,ax=plt.subplots(figsize=(8,4.4))
    top=familias.head(5).iloc[::-1]
    ax.barh(top.familia,top.valor_observado_clp/1e6,color="#235e75")
    ax.set_xlabel("Valor de adquisición observado (millones de CLP)")
    ax.set_title("Melipeuco: familias con mayor valor observado")
    for i,v in enumerate(top.valor_observado_clp/1e6):
        ax.text(v+0.8,i,f"{v:.1f}",va="center",fontsize=9)
    ax.set_xlim(0,top.valor_observado_clp.max()/1e6*1.18)
    fig.tight_layout()
    fig.savefig(OUT/"a_valor_observado.png",dpi=160)
    plt.close(fig)

    # B: acciones declaradas. Los montos son estimaciones, no pagos.
    acciones["completa"]=acciones.NIV_IMPLEM.eq("Implementación completa: 100%")
    dims=(acciones.groupby("DIMENSION",dropna=False)
        .agg(acciones=("RBD","size"), escuelas=("RBD","nunique"),
             estimacion_mediana_clp=("ESTIM_TOTAL","median"),
             estimacion_total_clp=("ESTIM_TOTAL","sum"),
             fraccion_completa=("completa","mean")).reset_index())
    dims["porcentaje_completo"]=dims.fraccion_completa*100
    dims.to_csv(OUT/"b_resumen_dimensiones.csv",index=False)
    # Cobertura: sólo establecimientos activos y con matrícula positiva.
    elegibles=directorio[(directorio.ESTADO_ESTAB==1)&(directorio.MAT_TOTAL>0)].copy()
    elegibles["con_pme"]=elegibles.RBD.isin(acciones.RBD)
    cobertura=(elegibles.groupby("COD_DEPE")
        .agg(escuelas_directorio=("RBD","size"),escuelas_pme=("con_pme","sum")).reset_index())
    cobertura["cobertura_pct"]=100*cobertura.escuelas_pme/cobertura.escuelas_directorio
    cobertura.to_csv(OUT/"b_cobertura_dependencia.csv",index=False)

    por_escuela=(acciones.groupby("RBD")
        .agg(acciones=("fila_excel","size"),estimacion_total_clp=("ESTIM_TOTAL","sum"),
             fraccion_completa=("completa","mean")).reset_index())
    por_escuela=por_escuela.merge(
        directorio[["RBD","NOM_RBD","NOM_COM_RBD","COD_DEPE","MAT_TOTAL","ESTADO_ESTAB"]],
        on="RBD",how="left",validate="one_to_one",indicator=True)
    assert por_escuela._merge.eq("both").all()
    por_escuela["estimacion_por_alumno_clp"]=por_escuela.estimacion_total_clp/por_escuela.MAT_TOTAL.where(por_escuela.MAT_TOTAL>0)
    cisterna=por_escuela[por_escuela.RBD.isin(piloto.RBD)].copy()
    assert len(cisterna)==8
    cisterna.drop(columns="_merge").to_csv(OUT/"b_panel_cisterna.csv",index=False)

    # Sensibilidad que evita interpretar la cola como gasto confirmado.
    grandes=acciones.ESTIM_TOTAL>1_000_000_000
    assert grandes.sum()==19
    sensibilidad=pd.DataFrame([
        {"escenario":"Todos los registros","acciones":len(acciones),
         "estimacion_total_clp":int(acciones.ESTIM_TOTAL.sum()),
         "estimacion_media_clp":acciones.ESTIM_TOTAL.mean(),
         "estimacion_mediana_clp":acciones.ESTIM_TOTAL.median()},
        {"escenario":"Excluir acciones > $1.000 millones","acciones":int((~grandes).sum()),
         "estimacion_total_clp":int(acciones.loc[~grandes,"ESTIM_TOTAL"].sum()),
         "estimacion_media_clp":acciones.loc[~grandes,"ESTIM_TOTAL"].mean(),
         "estimacion_mediana_clp":acciones.loc[~grandes,"ESTIM_TOTAL"].median()},
    ])
    sensibilidad.to_csv(OUT/"b_sensibilidad_extremos.csv",index=False)

    fig,ax=plt.subplots(figsize=(8,4.4))
    plot=dims.sort_values("porcentaje_completo")
    ax.barh(plot.DIMENSION,plot.porcentaje_completo,color="#377f70")
    ax.set_xlim(0,75)
    ax.set_xlabel("Acciones declaradas completas (%)")
    ax.set_title("PME 2024: implementación declarada por dimensión")
    for i,row in enumerate(plot.itertuples()):
        ax.text(row.porcentaje_completo+0.7,i,f"{row.porcentaje_completo:.1f}%",va="center",fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT/"b_implementacion_dimensiones.png",dpi=160)
    plt.close(fig)

    metrics={
        "a":{"partidas":len(compras),"equipos_adquiridos":int(compras.cantidad.sum()),
             "valor_partidas_clp":int(compras.valor_clp.sum()),"valor_impreso_cgr_clp":176164029,
             "equipos_observados":len(observados),"valor_observado_clp":int(observados.valor_clp.sum()),
             "porcentaje_equipos_observados":100*len(observados)/int(compras.cantidad.sum()),
             "porcentaje_valor_observado":100*observados.valor_clp.sum()/176164029,
             "comodatos":len(comodatos),"coincidencias":len(cruce),
             "valor_coincidencias_clp":int(cruce.valor_clp.sum()),
             "observados_sin_serie":int(observados.serie.isna().sum()),
             "observados_sin_rbd":int(observados.rbd.isna().sum())},
        "b":{"acciones":len(acciones),"escuelas":acciones.RBD.nunique(),
             "acciones_piloto":len(piloto),"escuelas_piloto":piloto.RBD.nunique(),
             "accion_cero":int((acciones.ESTIM_TOTAL==0).sum()),
             "sep_ausente":int(acciones.ESTIM_SEP.isna().sum()),
             "duplicados_adicionales":int(acciones.duplicado_exacto_adicional.sum()),
             "acciones_extremas":int(grandes.sum()),
             "fraccion_estimacion_extremos":float(acciones.loc[grandes,"ESTIM_TOTAL"].sum()/acciones.ESTIM_TOTAL.sum()),
             "mediana_estimacion_clp":float(acciones.ESTIM_TOTAL.median()),
             "media_estimacion_clp":float(acciones.ESTIM_TOTAL.mean()),
             "fraccion_completa":float(acciones.completa.mean()),
             "escuelas_union_verificada":len(por_escuela)}
    }
    (OUT/"metricas.json").write_text(json.dumps(metrics,ensure_ascii=False,indent=2))
    print("A: comprados",metrics["a"]["equipos_adquiridos"],"observados",metrics["a"]["equipos_observados"],
          "coincidencias con comodato",metrics["a"]["coincidencias"])
    print("B: acciones",metrics["b"]["acciones"],"RBD",metrics["b"]["escuelas"],
          "piloto",metrics["b"]["acciones_piloto"],"acciones")
    print("Verificaciones: importes CGR, clave única en anexos, unión RBD y extremos, OK")
    return metrics

if __name__=="__main__":
    main()
