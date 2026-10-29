# Prompt — Feature 4: Reglas de superposición

**Rama:** `feature/reglas-superposicion` (sale de `feature/crear-reserva`)

## Contexto suministrado

- `AGENTS.md`, `.memoria/estado.md`.
- `Harness/specs.md` §4.2 (superposiciones, límites consecutivos, simultaneidad).
- Ejemplo numérico de la consigna.

## Instrucción (extractos)

De la especificación:

> **Superposiciones:** RECHAZAR superposiciones de reservas *activas* para la misma
> unidad. **Límites consecutivos:** PERMITIR reservas consecutivas (ej. fin a las 11:00 e
> inicio de la siguiente a las 11:00). **Simultaneidad:** PERMITIR reservas en el mismo
> horario si son para *distintas* unidades.

De la consigna:

> Ejemplo: con MIC-01 reservado de 10:00 a 11:00, rechazar 10:30 a 11:30 y permitir
> 11:00 a 12:00. MIC-02 puede reservarse de 10:00 a 11:00 aunque MIC-01 esté ocupado.

## Episodio 4.1 — El ejemplo de la consigna como prueba

El agente convirtió el ejemplo en un fixture (`mic01_de_10_a_11`) y escribió sobre él:
el rechazo 10:30–11:30, seis variantes de solapamiento (por el inicio, contenida, que la
contiene, idéntica, mismo inicio, mismo fin), turnos consecutivos en ambos sentidos, el
hueco exacto entre dos reservas y las cinco unidades a la misma hora. Rojo: 7 failed.

## Episodio 4.2 — Regla de intervalos semiabiertos

El agente implementó `buscar_conflictos` con la condición
`inicio < :fin AND :inicio < fin AND estado = 'activa'` (ADR-012), pensada para
reutilizarla en la consulta de disponibilidad. Verde: 40 passed.
