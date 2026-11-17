# Data Lens — Justificación del rediseño del frontend

**Comparación de la versión 2.0 con la interfaz integrada v3.7–3.8.2**

| Aspecto | Versión 2.0 | Rediseño v3.7–3.8.2 | Motivo del cambio |
|---|---|---|---|
| Enfoque | Presentaba primero porcentajes y problemas agregados. | Parte de la **exploración de activos** y permite bajar hasta un problema concreto. | Responder **qué recurso está fallando**, no solo cuántos problemas existen. |
| Visión general | Indicadores con poco contexto del origen. | **Resumen** con acceso a mapa, inventario y diagnóstico. | Facilitar la exploración sin perder la visión global. |
| Identificación del recurso | Resultaba difícil localizar el activo asociado a un resultado. | **Mapa de activos e inventario** para identificar buckets, tablas y procesos. | Ubicar el problema en un recurso específico. |
| Investigación | Controles y métricas relativamente aislados. | **Ficha técnica** con configuración, relaciones y hallazgos del activo. | Mostrar el contexto necesario antes de interpretar un resultado. |
| Diagnóstico | Predominaba la lista general de hallazgos. | Consolida resultados y permite llegar **filtrado por el activo seleccionado**. | Conectar la investigación del recurso con la vista transversal de controles. |
| Detalle | Menor continuidad entre indicador y caso específico. | **Verificación → evidencia → interpretación → recomendación**. | Dar trazabilidad a cada problema mostrado. |
| Datos de demostración | Agregados y detalles podían no corresponderse. | Los indicadores se alimentan de un **escenario de registros unificados**. | Que los totales coincidan con resultados consultables. |
| Recorrido de uso | **Resultado general → lista de problemas**. | **Resumen → activo → ficha → hallazgo específico**; o directamente **Resumen → Diagnóstico → hallazgo**. | Permitir tanto exploración por recurso como revisión transversal. |
