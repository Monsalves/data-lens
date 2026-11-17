# Data Lens — Alcance inicial y arquitectura del prototipo

**Propuesta de MVP · 17 de noviembre de 2026 · documentación v5**

## Alcance inicial

Data Lens permitirá **descubrir activos de datos de una cuenta AWS y evaluar controles técnicos observables**, para pasar del Resumen a un recurso concreto, consultar su ficha y revisar los resultados asociados. La primera versión se centrará en **buckets S3, tablas almacenadas en S3 y catalogadas en Glue Data Catalog, Glue Jobs y sus ejecuciones, y recursos y tablas de Amazon Redshift**. Se consultarán configuraciones, metadatos y resultados de evaluaciones existentes que estén disponibles mediante los permisos otorgados. **Amazon DataZone es opcional**: puede aportar metadatos adicionales, pero no es necesario para descubrir estos servicios.

**Cuándo funciona:** un bucket S3 puede inventariarse y revisar su configuración **sin Glue**; para reconocer columnas o particiones de una tabla en S3 se requiere una definición accesible en **Glue Data Catalog**. Los **Glue Jobs** pueden revisarse aunque sus tablas de entrada y salida no estén catalogadas. **Redshift** puede descubrirse sin Glue ni DataZone, pero el detalle de sus bases, esquemas y tablas requiere acceso autorizado a los metadatos de la base de datos. La calidad de datos se mostrará **si existen resultados accesibles y vinculables**, como los de Glue Data Quality; no se asumirá que la simple existencia de una tabla prueba su calidad. Si faltan permisos o evidencia, la verificación quedará **sin acceso o no medida**. Por ahora se excluyen evaluaciones del contenido de documentos libres en S3, otras bases de datos (por ejemplo, MongoDB o RDS) y otras nubes.

## Stack tecnológico propuesto

| Componente | Tecnología | Justificación de la elección |
|---|---|---|
| Frontend | **React + TypeScript + Vite** | Permite llevar la interfaz HTML aprobada a componentes reutilizables, manteniendo navegación, filtros y estados consistentes. |
| Backend/API | **Python + FastAPI + Pydantic** | Facilita desarrollar endpoints tipados y definir un contrato claro entre frontend, escaneos y resultados. |
| Base de datos local | **SQLite + SQLAlchemy + Alembic** | Guarda inventario y evaluaciones sin administrar un servidor de base de datos durante el MVP; permite evolucionar el esquema. |
| Integración AWS | **boto3 + IAM/STS** | Usa el SDK oficial para consultar los servicios admitidos con permisos acotados. |
| Procesamiento de escaneos | **Worker Python** | Ejecuta descubrimiento y verificaciones sin bloquear las consultas de la interfaz. |
| Pruebas | **pytest + Playwright** | Comprueba cálculos, filtros y navegación desde un activo hasta su resultado. |

## Diagramas

### 1. Arquitectura local del MVP

[**Ver diagrama de arquitectura local**](https://monsalves.github.io/data-lens/documentacion/arquitectura/#arquitectura)

### 2. Sitemap completo — pantallas y navegación

[**Ver sitemap completo e interactivo**](https://monsalves.github.io/data-lens/documentacion/arquitectura/#sitemap)

[**Abrir documento interactivo**](https://monsalves.github.io/data-lens/documentacion/arquitectura/)

*Sitemap recuperado del diseño navegable v3.7 (39 nodos). Sus vínculos apuntan al prototipo publicado v3.8.2. Algunas pestañas son vistas internas, no pantallas independientes.*
