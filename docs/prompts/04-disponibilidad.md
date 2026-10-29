# Especificación técnica — Feature 4: Consulta de disponibilidad

**Rama:** `feature/disponibilidad`

## Qué se pidió (resumen)

Poder preguntar si una unidad está libre en un intervalo antes de reservar, con la
garantía de que la respuesta coincide con lo que haría la creación: si la consulta dice
"disponible", reservar ese intervalo tiene que funcionar, y al revés.

## Requisitos de entrada

- `Harness/specs.md` §4.1.1: consultar disponibilidad por unidad e intervalo, con las
  mismas reglas de superposición que la creación.
- Feature 3: `servicios.buscar_conflictos` ya implementa la regla.

## Decisiones y por qué

| Tema | Decisión | Motivo | Alternativa descartada |
| :--- | :--- | :--- | :--- |
| Regla | Reutilizar `buscar_conflictos` y el modelo `Intervalo` (ADR-012) | Una sola implementación: consulta y creación no pueden divergir | Una consulta SQL propia del endpoint |
| Forma del endpoint | `GET /unidades/{id}/disponibilidad?inicio=…&fin=…` | La disponibilidad es una propiedad de la unidad; `GET` porque no modifica nada | `POST /disponibilidad` con cuerpo |
| Respuesta | `disponible` + lista `conflictos` con las reservas que ocupan el intervalo (ADR-013) | La coordinación necesita saber quién ocupa el horario para reorganizar | Solo un booleano |
| Unidad inexistente | 404, porque la unidad es el recurso de la URL (ADR-013) | Al crear, la unidad viene en el cuerpo y es 422 (ADR-007) | 422 también acá |
| Intervalos pasados | Se pueden consultar (ADR-014) | Consultar no modifica nada y sirve para revisar el historial | Rechazarlos como en la creación |

## Criterios de aceptación (pruebas)

1. Unidad sin reservas → `disponible: true`, `conflictos: []`.
2. Intervalo superpuesto → `disponible: false` con el id de la reserva que choca.
3. Turno consecutivo y otra unidad a la misma hora → disponibles.
4. Consultar no crea reservas.
5. **Equivalencia:** para 7 intervalos alrededor de una reserva de 10:00 a 11:00,
   `disponible` coincide con que `POST /reservas` devuelva 201.
6. Unidad inexistente → 404; inicio ≥ fin, fecha inválida o parámetros faltantes → 422.

## Episodios

- **4.1 Prueba de equivalencia:** además de los casos puntuales, se escribió la prueba que
  compara consulta y creación sobre los mismos intervalos; 16 pruebas en rojo.
- **4.2 Implementación:** `consultar_disponibilidad` reutiliza la regla y el endpoint
  recibe el intervalo como modelo de query (`Annotated[Intervalo, Query()]`), así hereda
  las mismas validaciones de fechas; 58 pruebas en verde.
