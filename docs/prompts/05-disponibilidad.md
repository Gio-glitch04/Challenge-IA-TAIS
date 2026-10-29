# Prompt — Feature 5: Consulta de disponibilidad

**Rama:** `feature/disponibilidad` (sale de `feature/reglas-superposicion`)

## Contexto suministrado

- `AGENTS.md`, `.memoria/estado.md` (próximo paso: reutilizar `buscar_conflictos`).
- `Harness/specs.md` §4.1.1.

## Instrucción (extractos)

De la especificación:

> **Consultar disponibilidad:** Por unidad y por intervalo de tiempo. Debe respetar las
> mismas reglas de superposición que la creación.

De la consigna:

> La consulta de disponibilidad debe usar estas mismas reglas.

## Episodio 5.1 — Prueba de equivalencia

Además de los casos puntuales (libre, ocupado con conflicto, consecutivo, otra unidad,
404, 422), el agente escribió una prueba que verifica la *equivalencia*: para 7
intervalos alrededor de una reserva de 10:00 a 11:00, "disponible" debe coincidir
exactamente con "la creación devuelve 201". Rojo: 16 failed.

## Episodio 5.2 — Implementación reutilizando la regla

`servicios.consultar_disponibilidad` reutiliza `buscar_conflictos` y el endpoint recibe
el intervalo como modelo de query (`Annotated[Intervalo, Query()]`), así hereda las mismas
validaciones de fechas. Verde: 58 passed.
