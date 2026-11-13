# Alcance de los indicadores del frontend

Revisión local del 11 de noviembre de 2026. La interfaz calcula los 13 resultados con **fixtures sintéticos**; no hay lectura de una cuenta ni ejecución de estas operaciones. «Fuente prevista» significa que la API puede aportar el dato indicado si se integra, se concede acceso y existe la configuración necesaria. No afirma que esa integración esté implementada.

| ID | Indicador que muestra el mockup | Fuente prevista | Límite de la conclusión |
| --- | --- | --- | --- |
| M-01 | Activos con campo de responsable informado (16/20). | DataZone `GetAsset` y formulario asociado. | Un campo lleno no confirma que la persona asuma el rol. |
| M-04 | Solicitudes y grants por estado. | DataZone `ListSubscriptionRequests`, `ListSubscriptions`, `ListSubscriptionGrants`. | Los estados no prueban que el acceso sea adecuado. |
| M-07 | Campos requeridos que tienen valor (90/100). | DataZone `GetFormType` y `GetAsset`. | Presencia no equivale a exactitud del metadato. |
| M-09 | Conexiones de linaje registradas en el grafo de ejemplo (8). | DataZone `GetLineageNode`. | No hay denominador de tramos esperados: no se calcula cobertura ni se señalan faltantes. La captura de linaje debe estar habilitada y dentro del alcance consultado. |
| M-11 | Filas que fallan la regla de completitud (10/100). | Glue `GetDataQualityRuleset` y `GetDataQualityResult`, con métricas por regla. | La API entrega conteos por regla; los ID de fila del mockup son ilustrativos y no salen de esa respuesta. |
| M-16 | Ejecuciones terminales exitosas del job (18/20). | Glue `GetJobRuns`. | No mide calidad de los datos producidos ni otros jobs. |
| M-18 | Reglas configuradas con resultado (8/10). | Glue `GetDataQualityRuleset` y `GetDataQualityResult.RuleResults`. | Tener resultado no indica que el conjunto de reglas sea suficiente ni que las reglas pasen. |
| M-21 | Hallazgos activos de permisos no utilizados (8). | IAM Access Analyzer `ListFindingsV2`. | Solo describe el analizador y filtros consultados; no todos los permisos. |
| M-22 | Objetos inspeccionados con SSE-KMS informado (90/100). | S3 `HeadObject`. | SSE-S3 también cifra. Sin política aplicable no se afirma conformidad. |
| M-25 | Registros leídos con campos exigidos presentes (95/100). | S3 `GetObject` para leer el lote de logs. | No demuestra que se hayan capturado todos los eventos de auditoría. |
| M-26 | Activos con clasificación informada en catálogo (16/20). | DataZone `GetAsset` y formulario asociado. | No verifica exactitud ni vigencia de la clasificación. |
| M-27 | Casos sintéticos donde intervino el guardrail (18/20). | Bedrock `ApplyGuardrail`. | No se califica como acción correcta o cumplimiento; la batería no prueba eficacia general. |
| M-29 | Buckets consultados con regla de ciclo de vida activa (9/10). | S3 `GetBucketLifecycleConfiguration`. | No valida si el plazo de expiración cumple una política. |

Los porcentajes describen **el universo mostrado**, no la cuenta completa. Una conclusión de cobertura, conformidad o eficacia necesita además una referencia verificable y alcance suficiente. Data Lens puede descubrir automáticamente lo que la fuente expone, pero no debe inventar la referencia faltante.

## Documentación técnica contrastada

- [Linaje de DataZone](https://docs.aws.amazon.com/datazone/latest/userguide/datazone-data-lineage.html) y [GetLineageNode](https://docs.aws.amazon.com/datazone/latest/APIReference/API_GetLineageNode.html): conexiones registradas y condiciones para su captura.
- [GetAsset](https://docs.aws.amazon.com/datazone/latest/APIReference/API_GetAsset.html) y [GetFormType](https://docs.aws.amazon.com/datazone/latest/APIReference/API_GetFormType.html): valores y definición de formularios.
- [GetDataQualityResult](https://docs.aws.amazon.com/glue/latest/webapi/API_GetDataQualityResult.html): resultados y conteos agregados por regla.
- [ListFindingsV2](https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ListFindingsV2.html): hallazgos de un analizador especificado.
- [HeadObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_HeadObject.html): metadatos de cifrado del objeto.
- [ApplyGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ApplyGuardrail.html): acción observada para una entrada o salida enviada.
- [GetBucketLifecycleConfiguration](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketLifecycleConfiguration.html): reglas de ciclo de vida configuradas.
