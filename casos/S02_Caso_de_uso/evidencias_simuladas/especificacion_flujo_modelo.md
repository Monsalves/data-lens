> **SIMULADO · Banco Tinamú Digital (ficticio) · Tabla de trabajo ilustrativa. No es salida de AWS ni evidencia ejecutada en una cuenta real.**

# EV-06 · Diagrama de flujo de datos del modelo de preaprobación, v0.3 (documento simulado)

Autor: Arquitectura de Banco Tinamú Digital (ficticio). Fecha del documento: 26-oct-2026. Es la lista independiente de tramos esperados que usa EXA-04.
Nivel de detalle: tabla o bucket.

Tramos esperados (12):

1. `tnm-sim-aurora-originacion` → `tnm-sim-solicitudes-raw`
2. `tnm-sim-aurora-crm` → `tnm-sim-solicitudes-raw`
3. `tnm-sim-aurora-core` → `tnm-sim-solicitudes-raw`
4. `tnm-sim-solicitudes-raw` → `originacion.solicitudes_curado`
5. `originacion.solicitudes_curado` → `originacion.features_solicitante`
6. `tnm-sim-aurora-riesgo` → `riesgo.scoring_historico`
7. `riesgo.scoring_historico` → `originacion.features_solicitante`
8. `riesgo.ingresos_declarados` → `originacion.features_solicitante`
9. `tnm-sim-lago-analitico-a` → `originacion.ofertas_historicas`
10. `originacion.features_solicitante` → `tnm-sim-extractos-modelado-a`
11. `tnm-sim-extractos-modelado-a` → `tnm-sim-artefactos-modelo`
12. `tnm-sim-artefactos-modelo` → `modelo de preaprobación (destino)`
