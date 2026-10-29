# Especificación técnica — Feature 5: Cancelación y persistencia al reiniciar

**Rama:** `feature/cancelacion`

## Qué se pidió (resumen)

Cancelar una reserva sin perder su historial: el registro sigue en la base con su id y
sus datos, cambia su estado a "cancelada" y el horario vuelve a quedar libre. Además,
demostrar que reservas activas y canceladas sobreviven a detener y volver a levantar la
aplicación.

## Requisitos de entrada

- `Harness/specs.md` §4.1.3 (cancelar), §4.2 (las canceladas no bloquean), §4.3
  (persistencia) y §5.6 (prueba de cancelación).
- Consigna, "Verificaciones requeridas": persistencia comprobada de forma automática o con
  un procedimiento manual reproducible, con resultados esperados y observados.

## Decisiones y por qué

| Tema | Decisión | Motivo | Alternativa descartada |
| :--- | :--- | :--- | :--- |
| Qué hace cancelar | `UPDATE` de `estado` y `cancelada_en`; nunca `DELETE` (ADR-015) | Conserva el historial; como la regla de superposición filtra `activa` (ADR-009), el horario se libera sin código extra | Borrar la fila |
| Endpoint | `POST /reservas/{id}/cancelar` (ADR-016) | `DELETE` sugiere que el recurso desaparece, y acá se conserva | `DELETE /reservas/{id}` o `PATCH` con estado |
| Doble cancelación | 409 sin tocar `cancelada_en` (ADR-017) | Conserva la fecha original y avisa de un posible doble envío | Responder 200 de nuevo |
| Reservas pasadas | Se pueden cancelar (ADR-017) | La consigna no lo restringe y no afecta a ninguna regla | Rechazarlas |
| Historial | `GET /reservas?unidad_id=&estado=` con `estado` validado (`activa`/`cancelada`) | Permite ver activas y canceladas y verificar la persistencia | Sin listado |
| Verificación de reinicio | Prueba automática que levanta la app dos veces sobre el mismo archivo + procedimiento manual con Uvicorn real (ADR-018) | La consigna acepta cualquiera de las dos; con ambas queda cubierto el arranque real | Solo prueba unitaria |

## Criterios de aceptación (pruebas)

1. Cancelar → 200, estado `cancelada`, `cancelada_en` con fecha.
2. Después de cancelar, `GET /reservas/{id}` devuelve los mismos datos y la fila sigue en
   SQLite.
3. El mismo intervalo se puede volver a reservar y la disponibilidad lo marca libre.
4. Cancelar dos veces → 409; reserva inexistente → 404.
5. El listado muestra activas y canceladas y filtra por unidad y estado; estado desconocido → 422.
6. Tras reiniciar la app: la activa sigue `activa` y bloqueando, la cancelada sigue
   `cancelada` y liberada.

## Episodios

- **5.1 Pruebas de cancelación y de reinicio:** 11 pruebas nuevas; 10 en rojo (la de
  reserva inexistente ya daba 404 porque la ruta no existía).
- **5.2 Implementación y verificación manual:** cancelación en transacción y listado con
  filtros; 69 pruebas en verde. Después, procedimiento manual con Uvicorn real.
