# Prompt — Feature 6: Cancelación y persistencia al reiniciar

**Rama:** `feature/cancelacion` (sale de `feature/disponibilidad`)

## Contexto suministrado

- `AGENTS.md`, `.memoria/estado.md`.
- `Harness/specs.md` §4.1.3, §4.2 (canceladas no bloquean), §4.3 y §5.6.
- Consigna, sección "Verificaciones requeridas".

## Instrucción (extractos)

De la especificación:

> **Cancelar reserva:** Se debe conservar en la base de datos con su ID y todos sus datos,
> pero cambiando su estado a "cancelada". Al cancelar, el intervalo de tiempo vuelve a
> estar disponible.

De la consigna:

> Comprobar persistencia de reservas activas y canceladas tras detener y reiniciar sin
> borrar datos; esta última verificación puede ser automática o un procedimiento manual
> reproducible con resultados esperados y observados.

## Episodio 6.1 — Pruebas de cancelación y de reinicio

El agente escribió 10 pruebas de cancelación (estado, datos conservados, fila en SQLite,
horario liberado para reservar y en la disponibilidad, doble cancelación, 404, listado y
filtros) y una prueba de reinicio que levanta la app dos veces sobre el mismo archivo.
Rojo: 10 failed.

## Episodio 6.2 — Implementación y verificación manual

Cancelación con `UPDATE` dentro de una transacción, listado con filtros validados
(`Literal["activa", "cancelada"]`). Verde: 69 passed. Después ejecutó el procedimiento
manual con Uvicorn real: crear dos reservas, cancelar una, detener, volver a levantar y
listar.
