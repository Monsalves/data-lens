# Marco de trabajo para la evaluación de datos

Versión oficial 1.4 · Adoptada el 29 de octubre de 2026

La evaluación puede organizarse como una consulta médica: conocer el caso, ordenar los exámenes pertinentes, obtener sus resultados y emitir un diagnóstico. Se trabaja en un solo expediente con cuatro fichas y una matriz de vínculos. Cada dato se registra en su ficha de origen y se reutiliza en las fases siguientes.

## Recorrido de la evaluación

| Fase | Analogía | Ficha que se completa |
| --- | --- | --- |
| F0 | Historia del paciente | Cuenta y problema |
| F1 | Orden de exámenes | Plan de examen |
| F2 | Exámenes y resultados | Resultados y evidencia |
| F3 | Diagnóstico y tratamiento | Diagnóstico y acciones |

El prototipo es uno de los instrumentos de F2: obtiene evidencia y produce mediciones dentro de su capacidad validada. El evaluador elige los exámenes en F1 e interpreta sus resultados en F3. SQL, documentos o entrevistas pueden completar la evaluación.

## F0 Ficha de la cuenta y del problema

Completar una vez por evaluación. La cuenta incluye el contexto del cliente y sus datos; precisar las cuentas AWS cuando formen parte del alcance.

- **Identificación:** evaluación, fecha, evaluador y referentes de negocio y técnicos.
- **Problema y decisión:** qué ocurre, a quién afecta y qué se necesita decidir. Asignar un REQ por condición necesaria o pregunta derivada del problema.
- **Datos actuales:** fuentes y procesos relevantes, ubicación, formato o volumen conocido, actualización, responsable y sensibilidad. Registrar cada fuente una sola vez.
- **Condiciones de uso:** resultado esperado, plazos, restricciones y condiciones esenciales. Indicar quién declaró o confirmó la información.
- **Límites y dudas:** qué se incluye, qué se excluye y qué falta conocer, con responsable y siguiente paso.

**Salida:** contexto suficiente para decidir qué examinar. Una declaración del cliente todavía debe comprobarse cuando sea objeto de evaluación.

\pagebreak

## F1 Ficha del plan de examen

Seleccionar los exámenes según el problema de F0, comenzando por la oferta del prototipo que se presenta abajo. Una ficha de plan por evaluación reúne la selección y sus parámetros; el alcance común se toma de F0.

### Oferta teórica del prototipo

La tabla describe salidas que se propone implementar a partir de las APIs AWS investigadas y revisadas documentalmente el 29 de octubre de 2026. Su viabilidad se infiere de la documentación; su implementación y validación en cuenta están pendientes. Cada opción depende de los servicios, registros y permisos disponibles. La selección incluye solo las métricas pertinentes al caso.

| Pilar | Dimensión | Métrica y salida que podría entregar el prototipo |
| --- | --- | --- |
| Calidad | Reglas de calidad | **M-01 Nulos.** Cantidad y porcentaje de nulos por campo seleccionado, total evaluado y regla aplicada. Requiere consulta sobre datos accesibles o resultados de calidad con conteos suficientes; un porcentaje redondeado no permite deducir un conteo exacto. |
| Calidad | Reglas de calidad | **M-02 Antigüedad.** Diferencia entre fecha de contenido y fecha de evaluación; registros fuera del límite acordado. Requiere campo temporal, corte y zona horaria definidos. La fecha de modificación de una tabla no representa necesariamente la antigüedad de sus datos. |
| Calidad | Pipelines | **M-03 Ejecuciones y plazos.** Ejecuciones Glue por estado, inicio, fin y duración. Con calendario de entregas y evidencia de disponibilidad, podría contar entregas a tiempo, tardías y vencidas sin entrega. Un job exitoso por sí solo no acredita una entrega correcta. |
| Calidad | Curación | **M-04 Preparación y controles de salida.** Por lote identificable, pasos ejecutados y resultados de controles de calidad aprobados o fallidos, por separado. Requiere vincular lote, ejecución y evaluación; contar jobs no demuestra limpieza efectiva. |
| Responsabilidad | Responsables | **M-05 Atribución registrada.** Activos con y sin campo de propietario informado en Glue o formulario de DataZone; proyecto propietario registrado. La confirmación del responsable de negocio se registra cuando la aporta el referente. |
| Responsabilidad | Políticas de uso | **M-06 Concesiones registradas.** Solicitudes y concesiones de suscripción de DataZone por activo, destinatario y estado. Permite mostrar el respaldo técnico existente; no determina por sí solo que el uso tenga autorización contractual o consentimiento. |
| Visibilidad | Catálogo | **M-07 Metadatos.** Tablas o activos registrados, campos requeridos presentes y faltantes, y cantidades por campo. Con inventario de F0, fuentes sin correspondencia en el catálogo. Presencia de una descripción no acredita su exactitud. |
| Visibilidad | Linaje | **M-08 Recorridos registrados.** Nodos, conexiones de origen y destino y fechas disponibles en DataZone. Con recorridos esperados definidos, tramos respaldados y sin evidencia. Requiere captura previa; el inventario no reconstruye las transformaciones ausentes. |
| Acceso y seguridad | Acceso mínimo | **M-09 Permisos observados.** Concesiones de Lake Formation por principal, recurso y permiso. Con matriz autorizada, diferencias dentro del alcance consultado. Esta salida no representa todos los permisos efectivos de la cuenta AWS. |
| Acceso y seguridad | Protección | **M-10 Cifrado en S3.** Método y clave predeterminados por bucket; método por objeto o versión cuando se obtiene esa evidencia. Puede comparar con el requisito acordado. La configuración del bucket no prueba el cifrado de todo el histórico. |
| Acceso y seguridad | Protección | **M-11 Transporte seguro en S3.** Resultado de la regla de AWS Config que revisa la exigencia de SSL/TLS por bucket, con recurso y fecha de evaluación, si está disponible. No mide todas las conexiones de la plataforma. |
| Acceso y seguridad | Auditoría | **M-12 Eventos recuperables.** Eventos CloudTrail por identidad, acción, recurso y fecha; cantidades y campos faltantes. LookupEvents cubre administración e Insights de la región durante 90 días. Los eventos de datos requieren registros previamente habilitados y accesibles. |
| Cumplimiento y privacidad | Sensibles | **M-13 Detecciones en S3.** Hallazgos Macie por objeto y categoría, con resultados de inspección y errores disponibles. Puede contar objetos inspeccionados con detecciones; la cobertura depende del análisis existente y la ausencia de hallazgos no acredita ausencia de datos sensibles. |
| Cumplimiento y privacidad | Privacidad E/S | **M-14 Pruebas de contenido.** Para casos de entrada o salida definidos, acción y detecciones devueltas por ApplyGuardrail de Bedrock, indicando versión del guardrail. Requiere ejecutar pruebas; no acredita su integración en la aplicación ni la privacidad de todos los intercambios. |
| Cumplimiento y privacidad | Retención | **M-15 Conservación configurada en S3.** Reglas Lifecycle, filtros y plazos; modo y fecha de retención Object Lock por objeto o versión cuando aplique. Con política acordada, diferencias de configuración. No demuestra eliminación efectiva de versiones, réplicas o respaldos. |

Los IDs M-01 a M-15 conservan la correspondencia con el menú anterior; las salidas aquí descritas delimitan el aporte técnico propuesto. Las referencias del negocio son parámetros de la evaluación. Glue Data Quality y las consultas Athena formarían parte del prototipo si se implementan sus ejecuciones o lecturas; un SQL ejecutado por el evaluador fuera de esa integración se registra como revisión adicional. El resultado distingue evidencia no disponible, acceso denegado y periodo sin casos.

### Registro breve de los exámenes seleccionados

- **Examen y motivo:** ID CMP, REQ que atiende y condición o pregunta que se evaluará. Indicar si comprueba una condición o explora una situación.
- **Alcance:** fuente o proceso, unidad que se revisará, población o muestra y periodo. Explicar la selección de la muestra cuando exista.
- **Medición y referencia:** qué se medirá y cómo; regla o valor esperado, documento o dato de contraste con ubicación y versión, y quién lo confirma. Si es descriptivo, indicar la pregunta que debe responder.
- **Instrumento y evidencia esperada:** métrica del prototipo seleccionada y salida que se utilizará, o método de una revisión adicional. Conservar ubicación y versión del método sin repetir la tabla de oferta.
- **Preparación:** responsable, preparada o bloqueada y motivo. Anotar lo pendiente con siguiente paso; conservar versión, fecha y respaldo del acuerdo del plan.

### Revisiones adicionales

Si el caso requiere otra medición, definirla mediante el mismo bloque breve y asignarle un CMP propio, indicando «adicional». Registrar qué pregunta responde, qué medirá, método y responsable, alcance y periodo, referencia si corresponde y evidencia esperada. Sus resultados se incorporan en F2 y se enlazan en la misma matriz. No es obligatorio inventar un complemento para cada métrica del prototipo.

**Salida:** métricas del prototipo elegidas y revisiones adicionales justificadas, con parámetros y preparación. Conservar también bloqueos, diferimientos y exclusiones relevantes. No es necesario seleccionar las quince opciones.

\pagebreak

## F2 Ficha de resultados y evidencia

Una ficha de resultados por evaluación, con un bloque por resultado. Incorporar las salidas del instrumento y agregar la interpretación necesaria para leerlas.

- **Resultado y examen:** ID R, CMP y versión del plan aplicado; fecha y responsable de ejecución.
- **Observación:** qué se obtuvo, valor y unidad, cálculo o enlace al cálculo reproducible. Conservar la referencia de F1 y señalar cambios del plan antes de recalcular.
- **Evidencia:** ID EV, origen, ubicación recuperable, fecha de captura, periodo y método con versión y parámetros efectivos. Una misma evidencia puede servir a varios resultados.
- **Estado y cobertura:** Cumple, No cumple, No verificable o Sin casos en el periodo; indicar cuánto del alcance pudo verificarse y con qué límites. Una revisión descriptiva conserva observaciones sin estado de cumplimiento.
- **Limitaciones y pendientes:** accesos faltantes, errores, recortes, contradicciones o evidencia insuficiente; efecto, responsable y siguiente paso. Mantener visibles los exámenes bloqueados.

Cuando se cuenten unidades, registrar N total, C conformes, D con desviación y NV no verificables: N = C + D + NV. La cobertura es (C + D) / N si N > 0. Con universo desconocido, informar cantidades sin porcentaje; con N = 0 acreditado, informar Sin casos. La cobertura y el estado se leen por separado.

**Salida:** resultados sustentados, con evidencia consultable y límites explícitos. Una configuración del instrumento o una extracción de registros puede ser insuficiente para verificar la condición acordada.

\pagebreak

## F3 Ficha de diagnóstico y acciones

Completar una vez por evaluación, apoyándose en los resultados de F2.

- **Respuesta al problema:** qué puede concluirse para la decisión de F0 y qué condiciones siguen sin resolverse.
- **Diagnósticos:** ID DX, resultados R que lo sostienen, situación observada e impacto. Distinguir brecha demostrada, hipótesis y falta de información; incluir evidencia contraria o limitante.
- **Acciones:** ID AC, DX o bloqueo que atiende, qué hacer, responsable confirmado o propuesto, prioridad justificada, plazo y evidencia que permitirá cerrarla. Si procede mantener una condición, registrar esa decisión.
- **Alcance de la conclusión:** fuentes y periodo cubiertos, límites y condiciones futuras. Resumir por los cinco pilares reutilizando los resultados e indicando las exclusiones.

**Salida:** diagnóstico comprensible y próximos pasos. Los resultados del examen sustentan el diagnóstico; atribuir una causa requiere evidencia adicional cuando el examen no la demuestra.

## Matriz transversal de vínculos

La matriz funciona como índice del expediente. Se inicia con los REQ de F0 y se completa durante las cuatro fases. Contiene IDs o enlaces a los registros; las descripciones, reglas, mediciones y responsables permanecen en sus fichas de origen.

| F0 Requerimiento | F1 Examen | F2 Resultado y evidencia | F3 Diagnóstico | F3 Acción o decisión |
| --- | --- | --- | --- | --- |
| REQ-01 | CMP-01 | R-01 / EV-01 | DX-01 | AC-01 |

Una fila representa una relación. Un requerimiento puede tener varios exámenes y un resultado puede sostener varios diagnósticos: repetir el vínculo usando los mismos IDs. Contar objetos únicos. Las fases futuras quedan vacías; al corte, explicar los vínculos pendientes, excluidos o diferidos en su registro de origen.

## Ejemplo del recorrido completo

Ejemplo ficticio para mostrar la conexión entre fichas; los valores deben acordarse para cada caso.

**F0 · REQ-01.** El reporte llega tarde. El negocio confirma que debe estar disponible a las 08:00 en cada día hábil.

**F1 · CMP-01.** Comparar la hora de disponibilidad efectiva de las 20 entregas esperadas de un periodo acordado con las 08:00. Confirmar zona horaria y calendario. El prototipo aporta registros técnicos si su capacidad está validada; el evaluador completa la evidencia de disponibilidad cuando haga falta. Cada entrega debe cumplir el plazo.

**F2 · R-01 / EV-01.** Los registros revisados acreditan 15 entregas a tiempo y 5 tardías: N = 20, C = 15, D = 5, NV = 0. Estado No cumple y cobertura 20/20. El registro EV-01 conserva origen, archivo, captura y método.

**F3 · DX-01 / AC-01.** El reporte incumple el plazo en 5 entregas; la causa sigue abierta. Investigar el tramo que demora la disponibilidad, con responsable por confirmar, prioridad alta antes del próximo uso crítico y plazo propuesto de una semana. Cierre de esta acción de investigación: causa sustentada y propuesta de corrección. Verificar la corrección requerirá una nueva medición.

## Regla de aplicación

Un expediente, cuatro fichas y una matriz. Los pendientes se anotan donde afectan el trabajo; un listado separado se agrega solo si facilita coordinar el caso. Las consultas, fórmulas extensas y archivos del instrumento se adjuntan o enlazan. Los IDs nuevos pueden limitarse a REQ, CMP, R, EV, DX y AC; conservar los IDs existentes al reutilizar evaluaciones anteriores. Esta versión sustituye a la 1.3 como marco oficial del proyecto. Su aplicación práctica y las capacidades del prototipo siguen pendientes de validación.
