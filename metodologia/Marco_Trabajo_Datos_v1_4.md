# Marco de trabajo para la evaluación de datos

Versión oficial 1.4 · Adoptada el 29 de octubre de 2026 · Fichas alineadas con la plantilla final el 3 de noviembre de 2026

Este marco orienta una consultoría sobre la capa de datos de una organización que ya usa AWS. Se trabaja en un expediente con cuatro fichas y una matriz de trazabilidad. Las tablas siguientes son los registros que se completan en cada fase; el evaluador elige las comprobaciones y los criterios pertinentes para el problema de negocio. La [plantilla final en Google Sheets](https://docs.google.com/spreadsheets/d/1ffSsgFYO0LRBM4LXcJqXWCAGqYs_ry3qIkN11gYdRtg/edit) es la referencia de sus nombres y columnas.

| Fase | Pregunta que resuelve | IDs que se crean |
| --- | --- | --- |
| F0 · Cuenta y problema | ¿Qué problema, fuentes y condiciones debemos evaluar? | F, REQ |
| F1 · Plan de examen | ¿Qué se revisará, con qué criterio y cómo? | EXA |
| F2 · Resultados y evidencia | ¿Qué respaldo se obtuvo y qué indica frente al criterio? | EV, RES |
| F3 · Diagnóstico y acciones | ¿Qué puede concluirse y qué se hará? | DX, AC si corresponde |

## F0 Cuenta y problema

Completar una ficha por evaluación. Registrar el contexto declarado por el cliente, distinguir lo confirmado de lo pendiente e identificar cada fuente una sola vez. Los requisitos expresan condiciones o preguntas que importan para la decisión de negocio.

**Información a registrar**

| Campo | Información a registrar |
| --- | --- |
| Identificación | Evaluación, fecha, evaluador y referentes de negocio y técnicos. |
| Problema y decisión | Qué ocurre, a quién afecta y qué se necesita decidir. Asignar un REQ por condición necesaria o pregunta derivada del problema. |
| Datos actuales | Fuentes y procesos relevantes, ubicación, formato o volumen conocido, actualización, responsable y sensibilidad. Registrar cada fuente una sola vez. |
| Condiciones de uso | Resultado esperado, plazos, restricciones y condiciones esenciales. Indicar quién declaró o confirmó la información. |
| Límites y dudas | Qué se incluye, qué se excluye y qué falta conocer, con responsable y siguiente paso. |

**Preguntas sugeridas**

Estas preguntas ayudan a obtener la información anterior. No son una segunda ficha ni exigen respuestas duplicadas: registrar cada respuesta en el campo que corresponda.

| ID | Pregunta |
| --- | --- |
| P-01 | ¿Qué problema de negocio busca resolver y quién utilizará sus resultados? |
| P-02 | ¿Qué resultado de negocio se espera y con qué indicadores se reconocerá el éxito? |
| P-03 | ¿Qué fuentes necesita el caso de uso, dónde están y qué formatos y volúmenes tienen? |
| P-04 | ¿Qué dificultades existen para obtener los datos? ¿Qué tareas manuales o gestiones se requieren para conseguirlos? |
| P-05 | ¿Con qué frecuencia se actualizan hoy los datos y con qué frecuencia necesita que se actualicen? |
| P-06 | ¿Quién responde por cada fuente de datos y quién gestiona la autorización de su uso? |
| P-07 | ¿Qué información sensible contienen las fuentes y qué requisitos regulatorios condicionan su utilización? |

**Fuentes y activos**

| ID fuente | Fuente o activo | Ubicación | Formato | Actualización | Responsable y sensibilidad |
| --- | --- | --- | --- | --- | --- |
| F-__ |  |  |  |  |  |

**Requisitos**

| ID REQ | Fuente vinculada | Condición o pregunta | Propósito |
| --- | --- | --- | --- |
| REQ-__ | F-__ |  |  |

Un requisito puede considerar varias fuentes y una fuente puede servir a varios requisitos. Al reutilizar un ID, conservar claro a qué fuente se refiere cada vínculo. Una declaración del cliente no constituye por sí sola una comprobación.

## F1 Plan de examen

Crear un examen para cada comprobación necesaria. Debe responder a un REQ de F0 y señalar la fuente F que se revisará. El criterio se acuerda antes de interpretar el resultado; si el examen es descriptivo, indicar «sin umbral». Especificar en «Cómo se revisará» el método y el alcance necesario, como corte o población, cuando afecten la interpretación.

| ID Examen | REQ relacionado | Fuente datos relacionada | Comprobación | Criterio | Cómo se revisará |
| --- | --- | --- | --- | --- | --- |
| EXA-__ | REQ-__ | F-__ |  |  |  |

El ID EXA debe identificar sin ambigüedad el examen. Si se aplica la misma comprobación a otra fuente con un resultado independiente, darle otro ID o documentar explícitamente la relación entre fuente, ejecución y resultado. El instrumento puede ser un prototipo, una consulta, una revisión documental o una entrevista; no se presupone que esté implementado o validado en la cuenta.

## F2 Resultados y evidencia

Tras realizar el examen, registrar primero la evidencia EV y después el resultado RES que la interpreta. La salida de EV debe permitir recuperar el respaldo concreto, por ejemplo mediante un enlace, ruta o identificador de ejecución, además de indicar qué contiene. Un resultado puede apoyarse en varias evidencias: repetir su ID en la tabla EV sin duplicar el resultado.

**Evidencias**

| ID EV | Resultado relacionado | Instrumento revisión | Salida | Fecha en que se revisó |
| --- | --- | --- | --- | --- |
| EV-__ | RES-__ |  |  |  |

**Resultados**

| ID RES | EXA relacionado | Observación y valor | Regla aplicada | Estado |
| --- | --- | --- | --- | --- |
| RES-__ | EXA-__ |  |  |  |

La regla aplicada debe coincidir con el criterio de F1. «Cumple» o «No cumple» exige evidencia suficiente para la fuente y el alcance examinados. Si falta acceso, una referencia necesaria o respaldo suficiente, registrar «Sin evidencia suficiente» o «No verificable» y explicar el motivo en el registro o respaldo. «Sin casos» solo procede cuando se comprobó que la población del periodo fue cero. Un resultado descriptivo no necesita estado de cumplimiento.

## F3 Diagnóstico y acciones

Usar los resultados RES para redactar los diagnósticos DX. Primero completar la conclusión y su impacto o limitación; después registrar las acciones AC que correspondan. Un resultado favorable no obliga a crear una acción. Las causas no observadas se presentan como hipótesis, no como hechos demostrados.

**Diagnósticos**

| ID DX | Resultados relacionados | Conclusión | Impacto / limitación |
| --- | --- | --- | --- |
| DX-__ | RES-__ |  |  |

**Acciones**

| ID AC | Diagnóstico relacionado | Acción propuesta | Prioridad | Criterio de cierre | Estado |
| --- | --- | --- | --- | --- | --- |
| AC-__ | DX-__ |  |  |  |  |

La conclusión debe responder al problema de F0 dentro del alcance efectivamente revisado. En «Impacto / limitación» se distingue el efecto observado de lo que todavía no puede afirmarse. Una acción se cierra cuando existe el respaldo definido en su criterio de cierre; una propuesta no se presenta como ejecutada.

## Matriz de trazabilidad

La matriz muestra el recorrido de los IDs, no crea evidencia ni decide cumplimiento. Se llena con los registros existentes en F0 a F3. Una fila representa un camino sustentado; repetir IDs cuando haya varias evidencias, resultados, diagnósticos o acciones. Dejar la acción vacía cuando no corresponda.

| F0 Fuente | F0 Requisito | F1 Examen | F2 Resultado | F2 Evidencia | F3 Diagnóstico | F3 Acción |
| --- | --- | --- | --- | --- | --- | --- |
| F-__ | REQ-__ | EXA-__ | RES-__ | EV-__ | DX-__ | AC-__ o vacío |

Antes de concluir, comprobar que cada ID existe en su ficha, que la fuente de F1 corresponde al vínculo de F0, que EV respalda RES y que la regla de F2 es la acordada en F1. Los vínculos pendientes o excluidos deben poder explicarse. El expediente conserva las consultas, documentos y demás respaldos en ubicaciones recuperables.
