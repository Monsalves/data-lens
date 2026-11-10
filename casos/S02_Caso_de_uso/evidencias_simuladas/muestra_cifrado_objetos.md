> **SIMULADO · Banco Tinamú Digital (ficticio) · Tabla de trabajo ilustrativa. No es salida de AWS ni evidencia ejecutada en una cuenta real.**

# EV-12 · Muestra de cifrado de objetos (tabla simulada)

Fecha de la revisión: 05-nov-2026 (simulada). Muestra aleatoria; el requisito (supuesto): cifrado en servidor con la clave del banco.

| Bucket | Objetos en el inventario | Objetos revisados | Conformes | No conformes |
| --- | --- | --- | --- | --- |
| tnm-sim-extractos-modelado-a | 38.400 | 343 | 343 | 0 |
| tnm-sim-extractos-modelado-b | 52.100 | 343 | 339 | 4 |
| tnm-sim-solicitudes-raw | 96.300 | 343 | 340 | 3 |
| tnm-sim-solicitudes-curado | 71.800 | 343 | 343 | 0 |
| tnm-sim-clientes-baja | 118.200 | 343 | 338 | 5 |
| tnm-sim-decisiones-credito | 21.500 | 343 | 343 | 0 |
| tnm-sim-contratos | 14.300 | 342 | 342 | 0 |
| **TOTAL** | **412.600** | **2.400** | **2.388** | **12** |

Cobertura del inventario: 2.400 de 412.600 objetos (0,6 %), informada aparte como indica M-22.

## Objetos no conformes (12)

| Clave simulada | Bucket | Motivo |
| --- | --- | --- |
| tnm-sim-muestra/tnm-sim-extractos-modelado-b/obj-sim-0001 | tnm-sim-extractos-modelado-b | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-extractos-modelado-b/obj-sim-0002 | tnm-sim-extractos-modelado-b | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-extractos-modelado-b/obj-sim-0003 | tnm-sim-extractos-modelado-b | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-extractos-modelado-b/obj-sim-0004 | tnm-sim-extractos-modelado-b | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-solicitudes-raw/obj-sim-0005 | tnm-sim-solicitudes-raw | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-solicitudes-raw/obj-sim-0006 | tnm-sim-solicitudes-raw | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-solicitudes-raw/obj-sim-0007 | tnm-sim-solicitudes-raw | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-clientes-baja/obj-sim-0008 | tnm-sim-clientes-baja | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-clientes-baja/obj-sim-0009 | tnm-sim-clientes-baja | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-clientes-baja/obj-sim-0010 | tnm-sim-clientes-baja | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-clientes-baja/obj-sim-0011 | tnm-sim-clientes-baja | cifrado con clave gestionada por el servicio (no la del banco) |
| tnm-sim-muestra/tnm-sim-clientes-baja/obj-sim-0012 | tnm-sim-clientes-baja | cifrado con clave gestionada por el servicio (no la del banco) |
