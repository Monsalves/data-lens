# S02 · Aplicar la metodología a un caso de uso

**Caso ficticio: Banco Tinamú Digital (FSI en AWS).** Ejemplo para explicar la metodología 1.4 de punta a punta. Todo dato, resultado y evidencia es **ilustrativo y simulado**: no hay pruebas ejecutadas en AWS, el banco y las personas no existen, los criterios son supuestos y no se cita normativa.

| Archivo | Contenido |
| --- | --- |
| [Contexto_Caso_S02_Banco_Tinamu_Digital.md](Contexto_Caso_S02_Banco_Tinamu_Digital.md) | Documento de contexto del caso. Incluye «Cómo leer este ejemplo». Existe también en Word (`.docx`) en la copia local del proyecto; el repositorio publica solo Markdown. |
| [Plantilla_S02_Banco_Tinamu_Digital_rellena.xlsx](Plantilla_S02_Banco_Tinamu_Digital_rellena.xlsx) | Plantilla 1.4 rellena: Guía de uso, F0, F1, F2, F3 y Matriz. |
| [evidencias_simuladas/](evidencias_simuladas/) | 14 evidencias simuladas, una por ID EV de F2. |
| [herramientas/](herramientas/) | Modelo de datos y scripts que generan las cifras y comprueban la trazabilidad. |

## Cómo se genera y se comprueba

Con un Python que tenga `openpyxl` y `python-docx`, desde `herramientas/`:

1. `python generar_evidencias_y_plantilla.py` crea las evidencias y copia la plantilla publicada (`metodologia/Plantilla_Assessment_Datos_F0_F3.xlsx`); el original no se modifica.
2. `python generar_documento.py` crea el Markdown y el Word desde un único modelo de bloques.
3. `python verificar_caso_s02.py` lee los archivos entregados y comprueba IDs, vínculos F0 → F1, EV → RES, que la regla de F2 sea idéntica al criterio de F1, las cifras contra las evidencias y, si existe el Word, su sincronía con el Markdown.

## Plantilla de origen

Se copió la plantilla publicada `Plantilla_Assessment_Datos_F0_F3.xlsx`, que tiene la hoja «Guía de uso» y los IDs EXA y RES del marco 1.4.
