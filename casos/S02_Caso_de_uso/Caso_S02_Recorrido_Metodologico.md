# S02 · Banco Tinamú Digital: de los dolores al plan de examen

> **Caso ficticio para aprender a aplicar el marco 1.4.** El banco y sus personas no existen. Las cifras de la plantilla son ejemplos de cálculo, no mediciones en AWS. No se ejecutaron consultas, entrevistas ni solicitudes. Los umbrales son supuestos para mostrar cómo se acuerda un criterio; no representan una política real ni una exigencia normativa.

## Contexto y decisión

Banco Tinamú Digital quiere decidir si puede lanzar un modelo de preaprobación de créditos con datos de clientes. Su dirección necesita saber qué condiciones de la **capa de datos** debe revisar antes de tomar esa decisión. El assessment no evalúa la calidad del modelo, su equidad ni el cumplimiento normativo.

El cliente plantea tres dolores, todavía sin diagnosticar:

| Dolor expresado por el cliente | Lo que aún no se sabe | Decisión que necesita sustento |
| --- | --- | --- |
| «Cada área me entrega una lista distinta; no sé qué datos tengo ni quién responde por ellos». | Qué activos existen, cuáles faltan en el catálogo y quién es responsable. | Qué datos pueden usarse y qué falta ordenar antes del lanzamiento. |
| «La factura de AWS crece y no sé qué parte corresponde al modelo». | Cuánto se gasta por servicio y producto, y qué explica el cambio. | Si hay un problema de costo y dónde actuar. |
| «No sé si los datos de clientes están suficientemente protegidos». | Qué controles se aplican a los datos del alcance y qué no se pudo comprobar. | Qué riesgos requieren revisión antes del lanzamiento. |

Las frases son **declaraciones del cliente**, no hallazgos. F0 registra también las fuentes relevantes —catálogo, datos en S3, procesos de preparación, permisos, registros de auditoría y facturación—, quién puede facilitar cada una y los accesos pendientes. La plantilla rellena muestra ese registro con los IDs F y REQ.

## Cómo se aplica F0–F3

| Fase | Trabajo del evaluador en este caso | Salida en la plantilla |
| --- | --- | --- |
| **F0 · Cuenta y problema** | Convierte cada dolor en preguntas o condiciones que importan para decidir; delimita fuentes, responsables y dudas. | Fuentes F-01 a F-07 y requisitos REQ-01 a REQ-11. |
| **F1 · Plan de examen** | Elige una comprobación para cada requisito, define universo, periodo y criterio **antes** de conocer el resultado. | EXA-01 a EXA-11. Nueve usan métricas del catálogo; inventario y gasto son exámenes descriptivo y documental. |
| **F2 · Resultados y respaldo** | En una aplicación real, recupera la salida concreta de cada examen, calcula y compara con el criterio. Si falta acceso, registra el límite sin inventar un resultado. | RES-01 a RES-11. Las cifras de esta plantilla son únicamente ejemplos didácticos. Las filas EV ilustran qué respaldo se necesitaría; los archivos auxiliares son datos construidos para el ejemplo. |
| **F3 · Diagnóstico y acciones** | Separa lo observado de hipótesis y límites; propone acciones con responsable, prioridad y criterio de cierre. | DX-01 a DX-10 y AC-01 a AC-11, todas propuestas. |

### Tres recorridos que explican el método

**1. Control de activos.** El dolor sobre listas distintas se transforma en REQ-01 (saber qué existe) y REQ-02 (saber quién responde). EXA-01 compara inventario, catálogo y listas sin umbral; EXA-02 fija como criterio ilustrativo que al menos el 90 % de los activos catalogados tenga responsable. La plantilla usa el ejemplo de 31 de 40 activos (77,5 %): RES-02 queda «No cumple». DX-02 limita la conclusión a los activos catalogados y AC-02 propone completar responsables. El valor sirve para mostrar el cálculo y el vínculo entre fichas; no prueba que esos activos existan.

**2. Costos.** REQ-06 pregunta cuánto corresponde a cada servicio y producto. EXA-06 pide un desglose mensual de 12 meses. Como el escenario **no aporta ese desglose**, RES-06 termina «Sin evidencia suficiente». DX-05 no atribuye el aumento al modelo ni estima ahorro. AC-05 indica qué información habría que obtener. Una supuesta acta de solicitud no sustituye el desglose faltante.

**3. Seguridad.** REQ-09 pregunta por el cifrado de los datos de clientes. EXA-09 define qué objetos y configuración se revisarían, con un criterio ilustrativo de al menos 99 %. La plantilla muestra cómo se calcularía un resultado sobre una muestra ficticia: 2.388 de 2.400 (99,5 %). DX-07 aclara que esa cifra no permitiría afirmar «ciframos todo»: dejaría fuera otros almacenes y respaldos. Para REQ-11, el escenario no permite leer los registros de auditoría; RES-11 queda «No verificable» y AC-10 indica cómo habilitar el examen. Una supuesta acta de denegación tampoco reemplaza los registros.

## Qué debe mirar quien use la plantilla

Siga un ID desde el dolor en F0 hasta el examen F1, el resultado F2 y la conclusión F3. Observe en especial que **un estado favorable tiene alcance limitado**, que **la falta de acceso no se disfraza de medición** y que **una acción propuesta no es una corrección ejecutada**. La matriz reúne los vínculos entre fichas; no crea evidencia nueva.

La plantilla Excel rellena es el anexo de aplicación. Sus cifras y archivos auxiliares permiten recorrer un ejemplo consistente, pero no son evidencia de una evaluación real. Para aplicar el marco a una organización, habría que acordar sus propios criterios, ejecutar los exámenes autorizados y conservar las salidas reales recuperables.
