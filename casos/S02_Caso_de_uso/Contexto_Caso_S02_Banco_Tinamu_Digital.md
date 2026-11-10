# Caso de uso S02 · Banco Tinamú Digital

*¿Está el banco listo para lanzar un modelo de preaprobación de créditos? · Documento de contexto del caso · Versión 0.1 · 9 de noviembre de 2026*

> **Ejemplo ilustrativo.** El banco, las personas, las cifras, los resultados y las evidencias de este documento son ficticios y simulados para explicar la metodología 1.4. No es una evaluación real, no hay pruebas ejecutadas en una cuenta AWS y no se promete cumplimiento normativo ni se cita normativa concreta. Los criterios de aceptación son supuestos del cliente ficticio.

Este documento explica el contexto. Los datos del expediente (fuentes, requisitos, exámenes, evidencias, resultados, diagnósticos y acciones) están en la plantilla `Plantilla_S02_Banco_Tinamu_Digital_rellena.xlsx` y las evidencias simuladas en la carpeta `evidencias_simuladas/`.

## Cómo leer este ejemplo

El expediente sigue un solo hilo: **necesidad → criterio → evidencia → hallazgo → recomendación**. Cada paso tiene un ID que se puede buscar en la plantilla. La regla de lectura es: el examen (EXA) comprueba, la evidencia (EV) respalda, el resultado (RES) describe lo observado, el diagnóstico (DX) interpreta y la acción (AC) dice qué hacer.

Un recorrido completo, con los IDs reales del expediente:

| Paso | ID | Qué dice en este caso |
| --- | --- | --- |
| Necesidad (F0) | REQ-07 · F-02 | «Los datos de clientes y de crédito deben conservarse solo el tiempo que indica la política de conservación.» Nace de las preocupaciones de costos y seguridad. |
| Criterio (F1) | EXA-07 | Al menos el 90 % de los buckets con una regla de eliminación coherente con la política (métrica M-29). Acordado el 29-oct-2026, antes de revisar. Es un supuesto del cliente ficticio. |
| Evidencia (F2) | EV-09, EV-10 | Tabla de reglas por bucket y listado de objetos del bucket de clientes dados de baja. Ambas simuladas. |
| Resultado (F2) | RES-07 | 5 de 7 buckets conformes (71,4 %). Estado: No cumple. |
| Hallazgo (F3) | DX-06 | Dos buckets sin regla de eliminación; uno guarda datos de clientes dados de baja y nadie lo tiene en su lista. Riesgo observado; costo solo como hipótesis. |
| Recomendación (F3) | AC-07, AC-06, AC-08 | Primero proteger lo que sirva a una auditoría, luego separar lo que se conserva de lo que se elimina y al final eliminar. |

Otros finales posibles en el mismo expediente:

- **Favorable, sin acción:** REQ-09 → EXA-09 → RES-09 → DX-07. El cifrado de los objetos revisados cumple el criterio y no se crea ninguna acción.
- **No verificable:** REQ-11 → EXA-11 → RES-11 → DX-09 → AC-10. No se pudo leer el contenido de los registros de auditoría; el motivo queda explicado.
- **Sin evidencia suficiente:** REQ-06 → EXA-06 → RES-06 → DX-05 → AC-05. El gasto no se midió; las causas se presentan como hipótesis.
- **Descriptivo, sin umbral:** REQ-01 → EXA-01 → RES-01 → DX-01 → AC-01. Cuenta lo que existe y no emite estado de cumplimiento.

## 1. La organización y su situación

Banco Tinamú Digital es un banco digital ficticio, de tamaño mediano. No tiene sucursales: sus clientes abren cuentas, tarjetas y créditos de consumo desde una aplicación. Como referencia inventada para el ejemplo, tiene unas 600 personas y unos 380.000 clientes.

El banco usa una sola cuenta de AWS. Allí el equipo de Datos e IA mantiene un catálogo de datos, un data lake y los datos con que quiere entrenar un modelo que preapruebe créditos. La Gerencia General quiere lanzar ese modelo este trimestre, antes del 31 de diciembre de 2026. Antes de decidir quiere saber en qué estado están sus datos.

## 2. La decisión y las tres preocupaciones (P-01 y P-02)

**Problema y quién usa el resultado (P-01).** La Gerencia General y la Gerencia de Riesgo de Crédito usarán el resultado para decidir si lanzan el modelo.

**Decisión que depende del resultado.** ¿Está el banco listo para lanzar este trimestre un modelo de preaprobación de créditos y qué debe corregir antes?

**Las tres preocupaciones, tal como las declara el cliente:**

| Preocupación | En palabras del cliente | REQ que la descomponen en F0 |
| --- | --- | --- |
| 1. Control de activos | «No sé con exactitud qué datos tengo, dónde están ni quién responde por ellos. Cada área me entrega una lista distinta.» | REQ-01 a REQ-05 |
| 2. Costos | «La factura de AWS crece cada mes más que el negocio y nadie me dice qué parte es necesaria.» | REQ-06 a REQ-08 |
| 3. Seguridad | «No sé si estamos listos para poner un modelo que aprueba créditos con datos de clientes, y no quiero enterarme de un problema después.» | REQ-09 a REQ-11 |

**Creencias del cliente.** Se registran en F0 como declaradas y pendientes de confirmar. Una declaración no es una comprobación.

| Creencia | La declara | Qué examen la contrasta |
| --- | --- | --- |
| «El gasto sube por el modelo» | Gonzalo Bravo, Finanzas | EXA-06 (gasto por servicio y producto). Queda sin confirmar y sin descartar. |
| «Ciframos todo» | Daniela Pinilla, Tecnología | EXA-09 (cifrado de objetos). Se confirma para los objetos de S3 revisados; no se verificó en otros almacenes. |

**Resultado esperado e indicadores de éxito (P-02).** Se considera logrado si (a) la Gerencia General puede decidir con una lista clara de condiciones, (b) cada preocupación tiene una respuesta o un límite explícito y (c) cada acción tiene prioridad y criterio de cierre.

## 3. Actores y referentes

| Persona (ficticia) | Rol | Qué aporta o qué le importa |
| --- | --- | --- |
| Elena Marchetti | Gerenta General | Patrocina la decisión de lanzar el modelo. |
| Joaquín Arévalo | Gerente de Riesgo de Crédito | Usará el modelo; es responsable de negocio de los datos de originación y de scoring. |
| Daniela Pinilla | Gerenta de Tecnología | Administra la cuenta AWS, las bases y los permisos. |
| Rodrigo Velasco | Jefe de Datos e IA | Mantiene el catálogo, el data lake y los jobs que preparan los datos del modelo. |
| Natalia Ferrer | Oficial de Seguridad de la Información | Define el cifrado y administra los registros de auditoría; autoriza su lectura. |
| Gonzalo Bravo | Gerente de Finanzas | Recibe la factura de AWS. |
| Isabel Cornejo | Jefa de Cumplimiento | Debe indicar los plazos de conservación y los requisitos de privacidad. |
| Equipo evaluador | Aplica la metodología | Recoge la información, define exámenes y redacta el diagnóstico. Trabaja con un rol de solo lectura. |

## 4. Las fuentes de datos y su estado actual (P-03 a P-06)

**Qué fuentes necesita el caso, dónde están y qué formato tienen (P-03).** Son siete. El detalle por campo está en F0 de la plantilla; aquí solo se resume.

| ID | Qué es | Dónde está | Quién responde (declarado) |
| --- | --- | --- | --- |
| F-01 | Catálogo de datos corporativo (Amazon DataZone, dominio tnm-sim-datos) | AWS · us-east-2 · cuenta de ejemplo | Datos e IA (Rodrigo Velasco) |
| F-02 | Buckets S3 con datos de clientes, solicitudes y decisiones de crédito | S3 · us-east-2 · 5 buckets declarados (se confirman en EXA-01) | Datos e IA y Tecnología (por confirmar por bucket) |
| F-03 | Jobs ETL de AWS Glue que preparan los datos del modelo | Glue · us-east-2 · 6 jobs | Datos e IA (Rodrigo Velasco) |
| F-04 | Identidades y permisos IAM de la cuenta | IAM · cuenta 123456789012 | Tecnología (Daniela Pinilla) |
| F-05 | Registros de auditoría de la cuenta (CloudTrail) | S3 · bucket tnm-sim-auditoria-trail | Seguridad (Natalia Ferrer) |
| F-06 | Inventario de activos de datos: listas de Riesgo, Producto y TI, y descubrimiento en la cuenta | Hojas de cálculo de las áreas + servicios S3, Glue, Aurora/RDS y DynamoDB | Sin responsable único (se define con AC-01) |
| F-07 | Facturación mensual de AWS | Facturas en poder de Finanzas; consola de facturación sin acceso para el evaluador | Finanzas (Gonzalo Bravo) |

**Dificultades para obtener los datos (P-04).** Cada área guarda su lista de datos en hojas de cálculo propias y la entrega a pedido. Juntarlas toma varios días y varios correos. La factura de AWS llega a Finanzas como un documento mensual y hasta ahora no se ha pedido un reporte por producto. El contenido de los registros de auditoría solo lo lee Seguridad.

**Frecuencia de actualización (P-05).** Hoy las listas de las áreas se actualizan cuando alguien las pide. El catálogo se revisa cada mes. Los jobs de preparación corren a diario o cada hora. El modelo necesitaría datos de solicitudes al día (lo declara Riesgo). Para este ejemplo se supone que el inventario debe poder revisarse cada trimestre.

**Quién responde y quién autoriza el uso (P-06).** Datos e IA responde por el catálogo, el data lake y los jobs; Tecnología por la cuenta, las bases y los permisos; Seguridad por el cifrado y los registros de auditoría; Finanzas por la factura; Riesgo de Crédito por los datos de originación y de scoring; Cumplimiento por los plazos de conservación y la privacidad. Autoriza el uso de datos para el modelo Riesgo de Crédito junto con Cumplimiento (por confirmar). Quién responde por cada activo en particular es justamente una de las cosas que se examina (EXA-02).

## 5. Información sensible y requisitos regulatorios (P-07)

Las fuentes contienen datos personales y financieros de clientes: identificación, contacto, ingresos declarados e historial de crédito. Los requisitos regulatorios que condicionan su uso deben ser indicados por Cumplimiento. Este ejemplo no cita normativa ni promete cumplimiento. Los plazos de conservación que usa son supuestos del cliente ficticio:

- extracciones temporales para modelado: 30 días;
- solicitudes de crédito: 12 meses;
- datos personales de clientes dados de baja: 24 meses;
- decisiones de crédito y contratos: 60 meses.

## 6. El entorno AWS

- Una cuenta AWS (ID de ejemplo 123456789012, no real). Región principal us-east-2; el cliente dice que no hay otras regiones activas, pendiente de confirmar.
- Servicios que intervienen: Amazon S3, AWS Glue, Amazon DataZone (catálogo y linaje), Amazon Aurora/RDS, Amazon DynamoDB, IAM con su analizador de acceso no utilizado, AWS CloudTrail y un entorno de pruebas del modelo.
- Activos de datos que existen según el descubrimiento simulado: 48 (12 buckets, 26 tablas Glue, 4 bases Aurora/RDS y 6 tablas DynamoDB).
- Acceso del equipo evaluador: rol de solo lectura sobre el catálogo, Glue, IAM y la configuración de S3, y revisión de metadatos de una muestra de objetos. No tiene acceso al contenido de los registros de auditoría ni a la consola de facturación.
- Importante: no se ejecutó nada en AWS. Las consultas que menciona el plan de medición son plantillas sin ejecutar; los resultados de este caso son tablas simuladas.

## 7. Qué se midió y qué quedó fuera

Se usaron 9 métricas del piloto de 13, un examen descriptivo de inventario y un examen documental de gasto. Se respetan la fórmula, la unidad y el universo de cada métrica del plan de medición. M-21 es un conteo de hallazgos, no un porcentaje. Los criterios son supuestos del cliente ficticio, acordados antes de interpretar los resultados.

| Preocupación | REQ → EXA | Métrica (unidad) | Criterio supuesto | Resultado simulado | Estado final |
| --- | --- | --- | --- | --- | --- |
| 1 · Control de activos | REQ-01 → EXA-01 | Descriptivo | Sin umbral | 48 activos; 8 sin catálogo; 4 sin lista | Descriptivo (sin estado de cumplimiento) |
| 1 · Control de activos | REQ-02 → EXA-02 | M-01 (% cobertura) | ≥ 90 % | 31 de 40 (77,5 %) | No cumple |
| 1 · Control de activos | REQ-03 → EXA-03 | M-07 (% completitud) | ≥ 85 % | 176 de 200 (88,0 %) | Cumple |
| 1 · Control de activos | REQ-04 → EXA-04 | M-09 (% cobertura) | ≥ 80 % | 9 de 12 (75,0 %) | No cumple |
| 1 · Control de activos | REQ-05 → EXA-05 | M-26 (% cobertura) | ≥ 95 % | 34 de 40 (85,0 %) | No cumple |
| 2 · Costos | REQ-06 → EXA-06 | Documental (sin métrica) | Sin umbral; exige desglose de 12 meses | Gasto no medido | Sin evidencia suficiente |
| 2 · Costos | REQ-07 → EXA-07 | M-29 (% conformidad), indirecta | ≥ 90 % | 5 de 7 (71,4 %) | No cumple |
| 2 · Costos | REQ-08 → EXA-08 | M-16 (% éxito), indirecta | ≥ 90 % | 508 de 540 (94,1 %) | Cumple |
| 3 · Seguridad | REQ-09 → EXA-09 | M-22 (% conformidad) | ≥ 99 % | 2.388 de 2.400 (99,5 %) | Cumple |
| 3 · Seguridad | REQ-10 → EXA-10 | M-21 (conteo) | Máximo 5 hallazgos | 19 hallazgos | No cumple |
| 3 · Seguridad | REQ-11 → EXA-11 | M-25 (% completitud) | ≥ 98 % | Sin lectura de registros | No verificable |

**Por qué las otras cuatro métricas del piloto quedan fuera:**

| Métrica | Por qué no se usa en este caso |
| --- | --- |
| M-04 · Solicitudes y concesiones por estado | Responde cómo se tramitan los permisos de acceso a datos en DataZone. Ninguna de las tres preocupaciones lo pregunta, y en este caso el banco gestiona los accesos fuera de DataZone, así que la métrica no tendría universo. |
| M-11 · Nulos y ausentes | Mide la calidad del contenido de una tabla. Las tres preocupaciones se refieren a control, costos y seguridad, no al contenido. Queda como siguiente paso recomendable antes de entrenar el modelo. |
| M-18 · Cobertura de controles de salida | Necesita una lista previa de controles de calidad acordada con el cliente, que este caso no tiene; la calidad queda fuera de las tres preocupaciones. |
| M-27 · Casos infractores con acción esperada | Prueba filtros de privacidad de IA generativa con casos sintéticos y requiere autorización específica. El modelo de preaprobación no es generativo y no usa ese filtro. |

**Sobre el gasto.** Ninguna de las métricas aplicadas mide gasto. M-29 y M-16 son indicios indirectos (datos guardados de más y trabajo que podría repetirse), no mediciones del costo. Por eso el examen de gasto (EXA-06) termina como «Sin evidencia suficiente», el diagnóstico dice que el gasto no se midió y las causas se presentan como hipótesis. El ejemplo no incluye ninguna cifra de ahorro.

## 8. Restricciones, límites y dudas abiertas

| Duda o límite | Responsable | Siguiente paso |
| --- | --- | --- |
| Los plazos de conservación son supuestos del cliente ficticio. | Isabel Cornejo (Cumplimiento) | Validarlos antes de AC-06 y AC-08. |
| Que no haya otras regiones ni cuentas es lo que declara el cliente; no se verificó. | Daniela Pinilla (Tecnología) | Confirmarlo al repetir el inventario (AC-01). |
| No se leyó el contenido de los registros de auditoría. | Natalia Ferrer (Seguridad) | Acordar un acceso controlado de solo lectura (AC-10). |
| No se tuvo acceso a la facturación; el gasto no se midió. | Gonzalo Bravo (Finanzas) | Entregar el desglose mensual de 12 meses (AC-05). |
| No se sabe qué parte de los servicios de pruebas del modelo consume recursos hoy. | Rodrigo Velasco (Datos e IA) | Listar los servicios que usa el entorno de pruebas, como insumo de AC-05. |
| «Ciframos todo» se confirma solo para los objetos de S3 revisados; bases y respaldos no se revisaron. | Daniela Pinilla (Tecnología) | Decidir si se amplía el alcance en una segunda revisión. |
| La fecha de baja de cada cliente no está en S3; no se puede confirmar cuántos objetos pasaron el plazo de 24 meses. | Joaquín Arévalo (Riesgo de Crédito) | Aportar las fechas de baja como parte de AC-06. |
| No se evaluó la calidad del contenido de los datos ni el comportamiento o la equidad del modelo. | Gerencia General | Decidir si se incluyen en una segunda revisión. |

**Restricciones.** Plazo de la decisión: antes del 31 de diciembre de 2026. Trabajo con un rol de solo lectura. Todo dato, resultado y evidencia es simulado. Los criterios de aceptación son supuestos. No se cita normativa ni se afirma cumplimiento.

## 9. Dónde está cada cosa

- `Plantilla_S02_Banco_Tinamu_Digital_rellena.xlsx`: plantilla 1.4 rellena (Guía de uso, F0, F1, F2, F3 y Matriz).
- `evidencias_simuladas/`: 14 evidencias simuladas, una por cada ID EV de F2 (cada archivo lo indica en su primera línea).
- `herramientas/`: modelo de datos y scripts que generan las cifras y comprueban la trazabilidad (`verificar_caso_s02.py`).
