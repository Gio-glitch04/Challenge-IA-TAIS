# Prompt — Feature 3: Crear reserva con validaciones

**Rama:** `feature/crear-reserva` (sale de `feature/persistencia-inventario`)

## Contexto suministrado

- `AGENTS.md`, `.memoria/estado.md` (próximo paso: crear reserva).
- `Harness/specs.md` §4.1.2 y §4.2, y la consigna (sección "Decisiones y límites
  técnicos": documentar zona horaria, formato, fechas pasadas y límites).

## Instrucción (extracto de la especificación)

> **Crear reserva:** Requiere unidad (ID), solicitante ficticio, fecha/hora de inicio y
> fecha/hora de fin. Genera un identificador único de reserva. […]
> **Unidad:** Debe existir en el inventario precargado. **Solicitante:** No puede estar
> vacío ni compuesto solo por espacios. **Fechas/Horas:** Formato válido (ISO 8601). El
> inicio debe ser *estrictamente anterior* al fin.

Y de la consigna:

> Documentar zona horaria, formato de fechas, tratamiento de fechas pasadas y límites de
> duración o anticipación, si se aplican. Resolver lo no especificado con supuestos
> razonables y coherentes.

## Episodio 3.1 — Pruebas de entradas inválidas primero

El agente escribió `tests/test_crear_reserva.py` con casos de creación válida, id único,
consulta por id, 404, y entradas inválidas: solicitante vacío o solo espacios (3
variantes), inicio > fin, inicio == fin, unidad inexistente, 5 formatos de fecha no ISO,
fecha con zona horaria, fecha pasada y campos faltantes. Resultado en rojo: 21 failed.

## Episodio 3.2 — Supuestos no especificados

Antes de implementar, el agente definió y documentó los supuestos que la especificación
deja abiertos (ADR-008 a ADR-011): hora local sin zona, rechazo de reservas en el pasado,
sin límites de duración, 422 para unidad inexistente.

## Episodio 3.3 — Implementación

Modelos Pydantic con validadores, servicio `crear_reserva` dentro de una transacción
`BEGIN IMMEDIATE` y endpoints. Resultado: 27 passed.
