# GROUP_03_W1 - Workshop 1 de Business Intelligence

**Grupo:** 03. **Integrantes:** Javier Alcaíno, Lucas Riquelme y Renato Varela. **Versión:** 25-09-2026, Santiago. **Tema autorizado por el docente según información del grupo:** gasto educativo en Chile en lugar de las bases de salud sugeridas en la pauta. La autorización de tema no convierte las observaciones del análisis en feedback sobre sus conclusiones.

## Orden de lectura

1. `report/GROUP_03_W1_Report.pdf`: informe autónomo con dos candidatos, datos inspeccionados, comparación, preferencia, preguntas, Process record y referencias.
2. `analysis/W1_analisis_ejecutado.ipynb`: cuaderno guardado con tablas y figuras visibles, ejecutado de arriba abajo sobre los datos incluidos.
3. `analysis/outputs/`: CSV y PNG generados para revisar resultados sin abrir el cuaderno.
4. `data/PROCEDENCIA.md`: origen, unidades, versiones, transformación y límites de cada archivo.
5. `analysis/antecedentes/`: informe EDA navegable, diccionario, marco metodológico y scripts de extracción originales relevantes, como respaldo. Los scripts originales requieren fuentes grandes y la estructura del proyecto madre; el script W1 de esta carpeta es autónomo.

## Reproducir

Instalar las bibliotecas indicadas en `requirements.txt` en un entorno propio. Desde esta carpeta:

```sh
python -m pip install -r requirements.txt
python analysis/w1_analisis.py
python analysis/generar_informe.py
```

Luego abrir `analysis/W1_analisis_ejecutado.ipynb` con Jupyter y ejecutar todas las celdas desde el inicio. El cuaderno fue entregado con salidas guardadas; reejecutarlo sobrescribe las tablas y figuras de `analysis/outputs/` a partir de `data/`. Los caminos son relativos al paquete. El script usa Matplotlib en modo no interactivo. No requiere credenciales, conectores ni conexión de red.

Para auditar el origen de los CSV reducidos, consultar `data/PROCEDENCIA.md` y `data/fuentes_proyecto.json`; el informe CGR original y su extracción tabular están incluidos. El RAR de PME 2024 de 40 MB y el Directorio completo se pueden recuperar mediante las URL/versiones y huellas del manifiesto; el paquete incluye la selección de campos y el piloto inspeccionado.

## Alcance

Los valores PME son estimaciones declaradas y los bienes observados de Melipeuco describen una visita histórica. No se calculan pérdidas definitivas ni impacto SIMCE. El informe incluye los aportes individuales comunicados por el grupo. La reflexión individual no se incluye en esta versión.
