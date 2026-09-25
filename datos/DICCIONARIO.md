# Datos, unidades de análisis y limpieza

## Fuentes

La procedencia y huellas digitales están en `fuentes.json`. Los anexos CGR provienen del informe final 43/2024, reproducido por CIPER; el reporte nacional CGR fue descargado de una copia alojada por El Mostrador después de que el servidor oficial agotara el tiempo de espera. Son documentos producidos por Contraloría: el alojamiento no convierte la noticia del medio en la fuente numérica. La publicación oficial indexada corrobora los totales de Melipeuco. No se verificó criptográficamente la firma electrónica ni se obtuvo el expediente administrativo completo.

## Tablas principales

| Archivo CSV en procesados | Unidad y campos principales |
|---|---|
| `cgr_compras_lotes` | 29 filas de destino–documento–modelo. `cantidad`, `valor_clp` total de esa partida, `precio_unitario_clp=valor/cantidad`, fechas de factura/decreto. Una factura puede tener varias filas; no son 29 compras independientes. |
| `cgr_documentos_pago` | 21 combinaciones decreto–factura–fechas. El decreto de pago documentado por CGR no se reinterpreta como fecha de transferencia bancaria. |
| `cgr_no_habidos` | 628 observaciones de equipos: 625 del anexo 4, dos de tabla 3 y una de tabla 4. `observacion` distingue 10.a, 10.b y 10.c. `valor_clp` es valor bruto consignado por CGR, no valor actual. |
| `cgr_con_comodato` | 600 registros del anexo 5 con certificado de comodato; no son 600 equipos localizados. |
| `cgr_sin_comodato` | 144 registros del anexo 2. No contienen serie. Se conservan como unidades diferentes, aun cuando sus campos visibles se repitan. |
| `cgr_interseccion_comodato_no_habidos` | Coincidencia exacta por factura y serie normalizada entre anexos 4 y 5. No estima causalidad. |
| `cgr_limites_por_dependencia` | Límites marginales por destino para los 18 equipos sin distribución escolar individualizada. Los máximos de distintas escuelas no se suman. |
| `cgr_fuentes_financiamiento` | Seis filas de la tabla 2, transcritas y conciliadas con cantidad y monto oficiales. No se imputan automáticamente estos fondos a cada equipo. |
| `pme_acciones_nacional_2024` | 129.726 filas originales con selección de variables cuantitativas. `fila_excel` conserva la fila original, incluyendo encabezado. No existe un ID oficial de acción en el archivo. |
| `pme_panel_establecimientos_2024` | 8.240 RBD, agregados antes de unir al directorio. `estim_total`, `estim_sep`, `acciones`, `pct_completas`, `avance_min`, `avance_max`, `MAT_TOTAL`, `porc_ben`. |
| `pme_acciones_pilotos_2024` | Acciones de las dos comunas con descripción y columnas de financiamiento originales. |
| `pme_correlaciones` | Pearson y Spearman, con `n_pares` por pareja y escenario. Una observación es un establecimiento, no una acción repetida. |
| `pme_sensibilidad_montos` | Total/base, exclusión analítica de acciones >$1.000 millones, exclusión de duplicados exactos adicionales. No sustituye la base original. |
| `pme_faltantes`, `pme_cobertura_dependencia`, `verificaciones` | Diagnóstico de calidad y cobertura; controles de conservación. |

`id_fila`, `pagina_pdf`, `tabla` y `fila_tabla` permiten volver al documento. Las páginas PDF se numeran desde 1; las páginas impresas del informe principal suelen ser PDF menos 3. Se mantiene el texto original junto con las categorías analíticas.

## Decisiones que cambian el resultado

1. **Montos y fechas:** puntos de miles eliminados al convertir CLP a enteros. Fechas interpretadas día–mes–año. Sin ajuste IPC: se presentan valores históricos del inventario observado, no crecimientos reales del gasto.
2. **Celdas combinadas:** se completan sólo decreto, factura y fechas dentro de la misma dependencia cuando el PDF utiliza celdas combinadas. El relleno no se extiende entre escuelas.
3. **Página compartida:** la página PDF 63 termina el anexo 4 y empieza el 5. Se separan las dos tablas. Clasificar toda la página como un único anexo cambia los conteos en dos equipos y $284.410.
4. **Identidad escolar:** tabla 1 CGR, páginas PDF 7–8: Los Andes 6007; Molulco 6009; Fundo Molulco 6011; Cumcumllaque 6012; Carén 6017; Volcán Llaima 19927. Directorios 2021 y 2024 respaldan comuna y dependencia. Los dos Molulco tienen el mismo nombre en el directorio; no se unen por nombre. DEM y “Diferentes Establecimientos” permanecen sin RBD.
5. **Series:** mayúsculas, normalización Unicode y eliminación de espacios. “N° serie no identificado” se trata como ausente. No se convierte O en 0 ni se hacen coincidencias aproximadas. La intersección es conservadora ante errores de transcripción.
6. **Repetición:** los equipos sin serie no se deduplican: sus filas representan cantidades físicas. En PME hay cuatro filas exactamente repetidas adicionales; se marcan y conservan en el principal porque no existe ID que permita resolver si son acciones distintas. Se muestra sensibilidad al eliminarlas.
7. **Diferencias de la fuente:** suma de partidas de compras $176.164.030 frente a total impreso $176.164.029. Se conserva cada cifra; tasas globales usan el denominador publicado y tablas de partidas su suma. Valores por equipo redondeados pueden diferir de los totales del lote (Mlab: $1). Factura 2: anexo 1 dice 05-06-2021 y anexos 4/5 dicen 05-07-2021; las fechas originales no se sobrescriben. No afecta el enlace por factura/serie ni la conclusión sobre custodia.
8. **Faltantes PME:** 38 valores SEP ausentes; no se reemplazan por cero. La suma de componentes se calcula sólo si todos están presentes. `estim_sep` por escuela puede ser parcial si `faltantes_sep>0`; debe leerse con ese indicador.
9. **Valores extremos PME:** se conservan los 19 registros >$1.000 millones. El umbral es una decisión de sensibilidad explícita, no un umbral legal ni una clasificación de fraude. No se dividen cifras por mil sin documento que autorice la corrección.
10. **Directorio:** `MATRICULA` es indicador de presencia de matrícula; **no** cantidad de estudiantes. Para 2024 se usa `MAT_TOTAL`. El directorio 2021 descargado no trae ese conteo y sólo se utiliza para validar identidad.
11. **Uniones:** PME agregado por RBD → directorio 2024 con validación 1:1. Los 8.240 RBD encuentran correspondencia. Correlaciones y tasas por estudiante se restringen a estado activo y matrícula positiva: 8.237 escuelas. Se conservan las otras tres en el panel con `elegible=False`.
12. **Implementación:** los rangos 0, 1–24, 25–49, 50–74, 75–99 y 100 se conservan como intervalos. `pct_completas` es fracción de acciones al 100%, no porcentaje de avance ni ejecución financiera. `avance_min/max` son promedios simples de extremos, sin asignar un punto medio artificial.

## Interpretaciones que estas tablas no permiten

No equivalen a saldos SEP, rendiciones aceptadas, gasto fiscalizado nacional, matrícula de usuarios de equipos 2021, usuarios activos, efecto SIMCE ni pérdida fiscal firme. Los cero de montos declarados son valores observados, no evidencia de que una acción no se haya realizado. Ausencia de una serie en el anexo de no habidos no acredita buen uso; sólo ausencia de esa observación dentro del universo fiscalizado.

Las correlaciones describen la base publicada. No se calculan valores p de una supuesta muestra aleatoria: la cobertura está seleccionada y las acciones de una misma escuela no son independientes. Las tasas de Melipeuco describen el universo auditado; no se extrapolan a Chile.
