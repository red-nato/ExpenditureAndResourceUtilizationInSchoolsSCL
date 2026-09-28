# Diccionario operativo de las cinco fuentes

Este diccionario corresponde al paquete W1 del 25-09-2026. La incorporación posterior de OC ChileCompra y el estado explícito de materia PAS están en el [diccionario vigente del análisis principal](../../../datos/DICCIONARIO.md); no se infiere materia PAS a partir de `actividad` o `programa`.

| Fuente | Fila y período | Identificador propuesto y prueba | Campos usados | Faltantes y límite |
|---|---|---|---|---|
| Directorio Mineduc | Un establecimiento en un año; 2022–2025 | `(anio, rbd)`; unicidad comprobada en `perfil_fuentes.csv` y `controles_etapas.csv` | `dependencia`, `oferta`, `matricula_total`, `sostenedor_rut_sin_dv` | El censo incluye funcionamiento, matrícula positiva y dependencia pública/particular subvencionada. 60/60/59/59 RBD por año. |
| PAS Supereduc | Un proceso publicado en archivo anual; 2022–2025 | `pa_id`; unicidad comprobada. `(archivo_anio, rbd)` sirve para agrupar, no es llave de fila | `actividad`, `programa`, `estado`, `instancia`, `multa_primera`, `reintegro_primera`, `resolucion_termino` | No contiene materia financiera detallada ni rendición. `archivo_anio`, ingreso y término pueden diferir. Cero filas PAS no significa cero fiscalizaciones. |
| PME Mineduc | Una acción declarada en 2024 | `fila_excel` es localizador de la extracción, no ID oficial de acción. Unicidad comprobada; RBD puede repetirse | `RBD`, `DIMENSION`, `ESTIM_TOTAL`, `ESTIM_SEP`, `NIV_IMPLEM` | Monto estimado, no gasto ejecutado. La ausencia de fila exige verificar aplicabilidad y cobertura. |
| SIMCE Agencia | Una fila pública por RBD, año y grado aplicado; 2023–2025 | `(anio, rbd, grado)`; unicidad comprobada | `medidas_originales` con `prom_*`, `nalu_*`, `dif_*`, `sigdif_*`; `version_base`, GSE | Fila sin puntaje y establecimiento sin aplicación son casos distintos. Algunas versiones son preliminares. |
| IDPS Agencia | Una fila pública por RBD, año, grado e indicador; 2023–2025 | `(anio, rbd, grado, indicador_codigo_original)`; unicidad comprobada | `promedio_original`, `diferencia_original`, `significancia_original`, `version_base`, GSE | No comparar años/grados/indicadores como si fueran un único resultado; promedio ausente no es cero. |

**Llaves antes del cruce.** Las llaves anteriores fueron hipótesis de modelado. La etapa `Profile` contó duplicados y la etapa `Validate` impidió publicar el panel si había repetición, RBD ajeno al censo anual o pérdida de filas al agregar. Las transformaciones permanecen en `analysis/pipeline_la_cisterna.py`.

**Rendición pendiente.** El futuro archivo financiero debe tener como mínimo `RBD + ejercicio + subvención + cuenta + versión/estado de rendición`; no se le asigna llave definitiva hasta inspeccionar su diccionario y duplicados. Una transacción requiere su propio ID, no basta RBD.
