# Semana 3 · Mapa preliminar de servicios AWS

**Estado:** borrador incompleto. Los servicios son candidatos para evaluar una capa de datos ya alojada en AWS; todavía no se han validado en una cuenta.

## Mapa preliminar

| Pilar | Dimensión | Servicio AWS candidato |
| --- | --- | --- |
| Responsabilidad | Responsables | AWS Glue Data Catalog; Amazon DataZone; AWS Config |
| Responsabilidad | Políticas de uso | Amazon DataZone; AWS Lake Formation |
| Visibilidad | Catálogo | AWS Glue Data Catalog; Amazon DataZone |
| Visibilidad | Linaje | Amazon DataZone; AWS Glue |
| Calidad | Reglas de calidad | AWS Glue Data Quality; Amazon Athena |
| Calidad | Pipelines | AWS Glue; Amazon CloudWatch |
| Calidad | Curación | AWS Glue Data Quality; Amazon S3 |
| Acceso y seguridad | Acceso mínimo | IAM Access Analyzer; AWS Lake Formation |
| Acceso y seguridad | Protección | Amazon S3; AWS KMS; AWS Config |
| Acceso y seguridad | Auditoría | AWS CloudTrail; Amazon S3 |
| Cumplimiento y privacidad | Sensibles | Amazon Macie; Amazon DataZone |
| Cumplimiento y privacidad | Privacidad E/S | Amazon Bedrock Guardrails |
| Cumplimiento y privacidad | Retención | Amazon S3 Lifecycle; S3 Object Lock |
