# S02 · Aplicar la metodología a un caso de uso

**Caso ficticio: Banco Tinamú Digital (FSI en AWS).** Ejemplo para explicar cómo se pasa de los dolores del cliente al plan de examen y al diagnóstico del marco 1.4. Comienza por [el recorrido metodológico](Caso_S02_Recorrido_Metodologico.md) y luego consulta la plantilla rellena. Ningún dato o resultado procede de una evaluación real ni de AWS.

| Archivo | Contenido |
| --- | --- |
| [Caso_S02_Recorrido_Metodologico.md](Caso_S02_Recorrido_Metodologico.md) | Documento principal: contexto, tres dolores y cómo se aplican F0–F3. [Ver en el portal](https://monsalves.github.io/data-lens/caso-s02/). |
| [Plantilla_S02_Banco_Tinamu_Digital_rellena.xlsx](Plantilla_S02_Banco_Tinamu_Digital_rellena.xlsx) | Anexo de aplicación: fichas F0–F3 y Matriz rellenas con cifras ilustrativas. [Ver en el portal](https://monsalves.github.io/data-lens/caso-s02/plantilla/). |
| [evidencias_simuladas/](evidencias_simuladas/) | Doce archivos de datos construidos para comprobar los cálculos del ejemplo. No hay actas de gestiones ficticias. Los exámenes de gasto y auditoría figuran sin respaldo en la plantilla. |
| [herramientas/](herramientas/) | Modelo de datos, generador del anexo y verificador de trazabilidad. |

## Cómo se genera y se comprueba

Con un Python que tenga `openpyxl`, desde `herramientas/`:

1. `python generar_evidencias_y_plantilla.py` crea los datos simulados y copia la plantilla publicada (`metodologia/Plantilla_Assessment_Datos_F0_F3.xlsx`); el original no se modifica.
2. `python verificar_caso_s02.py` lee los archivos entregados y comprueba IDs, vínculos F0 → F1, EV → RES, criterios, cifras y los dos caminos que quedan sin respaldo.

## Plantilla de origen

Se copió la plantilla publicada `Plantilla_Assessment_Datos_F0_F3.xlsx`, que tiene la hoja «Guía de uso» y los IDs EXA y RES del marco 1.4.
