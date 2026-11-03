# Semana 3 · Servicios AWS para evaluar la capa de datos

**Estado:** borrador incompleto, 3 de noviembre de 2026. Investigación documental inicial. **No se ha ejecutado una prueba en una cuenta AWS.**

## Propósito y criterio de selección

El assessment se dirige a una empresa FSI que ya tiene datos y servicios en AWS. El punto de partida es el inventario de fuentes de F0 y las preguntas de F1. El mapa de abajo identifica servicios que *podrían aportar evidencia* por pilar y dimensión; no exige activar todos los servicios ni convierte las métricas en un catálogo obligatorio.

La estructura de pilar y dimensión se toma de la [hoja de referencia «Trazabilidad Pregunta»](https://docs.google.com/spreadsheets/d/1KHVM0JyYWwN8I-pdt1Aa-h3G_PBd3sFY3L-KBs37uGA/edit?gid=1654958782#gid=1654958782). Sus métricas M-01 a M-29 son candidatas en discusión y no forman parte de la metodología oficial 1.4. Existe además un Excel interno de investigación anterior M-01 a M-15; sus identificadores responden a otro catálogo y no deben mezclarse con los de la hoja de referencia.

## Mapa preliminar

| Pilar | Dimensión | Servicio AWS candidato | Qué se buscaría observar | Estado |
| --- | --- | --- | --- | --- |
| Responsabilidad | Responsables | AWS Glue Data Catalog; Amazon DataZone; AWS Config | Responsable declarado para cada fuente; etiquetas de recursos como apoyo | Pendiente de contrastar con responsables del cliente |
| Responsabilidad | Políticas de uso | Amazon DataZone; AWS Lake Formation | Solicitudes, suscripciones y concesiones frente al uso autorizado | Pendiente de política y permisos efectivos |
| Visibilidad | Catálogo | AWS Glue Data Catalog; Amazon DataZone | Activos, esquema y metadatos requeridos | Pendiente de inventario F0 y campos exigidos |
| Visibilidad | Linaje | Amazon DataZone; AWS Glue | Tramos de origen, transformación y destino capturados | Pendiente de comprobar instrumentación y cobertura |
| Calidad | Reglas de calidad | AWS Glue Data Quality; Amazon Athena | Resultados de reglas y consultas sobre datos en alcance | Pendiente de reglas, población y ejecución |
| Calidad | Pipelines | AWS Glue; Amazon CloudWatch | Estado, fecha y duración de ejecuciones | Pendiente de elegir procesos y ventana |
| Calidad | Curación | AWS Glue Data Quality; Amazon S3 | Controles de salida y resultados antes/después de preparar datos | Pendiente de vincular lotes comparables |
| Acceso y seguridad | Acceso mínimo | IAM Access Analyzer; AWS Lake Formation | Hallazgos de acceso y concesiones sobre datos | Pendiente de definir necesidad funcional autorizada |
| Acceso y seguridad | Protección | Amazon S3; AWS KMS; AWS Config | Cifrado y reglas de transporte de recursos en alcance | Pendiente de política, objeto/versión y configuración |
| Acceso y seguridad | Auditoría | AWS CloudTrail; Amazon S3 | Tipos de eventos capturados y registros recuperables | Pendiente de configuración, ventana y eventos de datos |
| Cumplimiento y privacidad | Sensibles | Amazon Macie; Amazon DataZone | Descubrimiento S3 y clasificación registrada | Pendiente de cobertura y confirmación de clasificación |
| Cumplimiento y privacidad | Privacidad E/S | Amazon Bedrock Guardrails | Respuestas de controles a un corpus de prueba de entradas y salidas | Solo si el caso usa IA generativa; pendiente de corpus |
| Cumplimiento y privacidad | Retención | Amazon S3 Lifecycle; S3 Object Lock | Reglas configuradas de expiración o conservación por versión | Pendiente de política y prueba de disposición efectiva |

**Lectura:** los servicios de la tabla son candidatos documentales. Un resultado de API, una etiqueta o una configuración por sí solos pueden ser evidencia parcial. Las dimensiones «Privacidad E/S» y «Retención» solo entran en el examen si F0 confirma que aplican al caso.

## Acceso que se debe solicitar para validar

Solicitar al dueño de la cuenta un **rol temporal de evaluación de solo lectura**, con cuenta y regiones definidas, vigencia y trazabilidad de uso. Adjuntar el inventario de fuentes F0 y elegir únicamente las filas del mapa aplicables. Para cada servicio elegido, acordar recursos concretos, operaciones de consulta, permisos IAM y, cuando corresponda, permisos de Lake Formation, del catálogo, de KMS o del motor SQL. Pedir acceso a un conjunto de prueba o una muestra autorizada y al destino de resultados si se ejecutarán consultas. La autorización de IAM no acredita acceso al dato cuando intervienen otros controles.

| Dato para la solicitud | Por completar con el cliente |
| --- | --- |
| Cuenta, regiones y referente AWS | Pendiente |
| Fuentes F0 y recursos/ARN en alcance | Pendiente |
| Rol asumible, duración y mecanismo de acceso | Pendiente |
| Servicios y operaciones de lectura por escenario | Pendiente |
| Permisos de datos y conectividad adicional | Pendiente |
| Ventana, costos, restricciones y aprobación de pruebas | Pendiente |

**Texto base para solicitar el acceso:** «Solicitamos un rol temporal de evaluación para la cuenta [ID] en [regiones], limitado a los recursos [ARN o nombres] y a las operaciones de lectura de [servicios seleccionados]. El objetivo es verificar [preguntas de F1] con [muestra autorizada] durante [ventana]. Confirmen el referente técnico, los permisos de datos adicionales, la conectividad necesaria y el límite de consumo antes de programar las pruebas». La lista exacta de acciones y recursos se adjuntará después de seleccionar las rutas aplicables del mapa.

Antes de solicitar o ejecutar pruebas, el administrador debe revisar la política de mínimo privilegio por recurso. Las pruebas que crean analizadores, reglas, jobs o consultas con costo requieren acuerdo explícito sobre entorno y consumo. Existe una solicitud de accesos detallada en la investigación interna anterior; sirve como antecedente, no como solicitud enviada.

## Pendientes para cerrar S03

1. Confirmar las fuentes F0 y seleccionar las dimensiones pertinentes.
2. Completar por ruta la operación o consulta exacta, los permisos y los límites de evidencia.
3. Obtener la cuenta y el rol; ejecutar pruebas acotadas y registrar resultado, fecha, región, recurso y evidencia recuperable.
4. Revisar con el cliente si la evidencia responde a cada pregunta de F1. Solo entonces declarar una ruta técnicamente validada.

## Fuentes AWS consultadas

- [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html) y [monitoreo de jobs](https://docs.aws.amazon.com/glue/latest/dg/view-job-runs.html).
- [Amazon DataZone: linaje](https://docs.aws.amazon.com/datazone/latest/userguide/datazone-data-lineage.html) y [suscripciones](https://docs.aws.amazon.com/datazone/latest/userguide/approve-reject-subscription-request.html).
- [IAM Access Analyzer: hallazgos](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html) y [permisos Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/lf-permissions-overview.html).
- [AWS CloudTrail: eventos de datos](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html), [AWS Config: etiquetas requeridas](https://docs.aws.amazon.com/config/latest/developerguide/required-tags.html) y [Amazon Macie: descubrimiento](https://docs.aws.amazon.com/macie/latest/user/data-classification.html).
- [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-how.html), [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) y [S3 Lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html).
