# Especificación técnica — Feature 3: Reglas de superposición

**Rama:** `feature/reglas-superposicion`

## Qué se pidió (resumen)

Que una unidad no pueda quedar reservada dos veces en horarios que se pisan, sin bloquear
los casos válidos: turnos pegados (uno termina cuando empieza el otro) y la misma franja en
unidades distintas. La regla tiene que quedar en un solo lugar, porque la consulta de
disponibilidad (feature 4) debe aplicar exactamente la misma.

## Requisitos de entrada

- `Harness/specs.md` §4.2: rechazar superposiciones de reservas activas de la misma
  unidad, permitir límites consecutivos y simultaneidad entre unidades distintas.
- Ejemplo de la consigna: con MIC-01 de 10:00 a 11:00, rechazar 10:30–11:30, aceptar
  11:00–12:00 y aceptar MIC-02 de 10:00 a 11:00.

## Decisiones y por qué

| Tema | Decisión | Motivo | Alternativa descartada |
| :--- | :--- | :--- | :--- |
| Modelo de intervalo | Semiabierto `[inicio, fin)`: chocan si `existente.inicio < nueva.fin AND nueva.inicio < existente.fin` (ADR-009) | Con desigualdad estricta los turnos consecutivos no chocan y cualquier solapamiento real sí | Intervalo cerrado `[inicio, fin]`, que rechaza los consecutivos |
| Qué reservas cuentan | Solo `estado = 'activa'` (ADR-009) | Deja listo que las canceladas no bloqueen (feature 5) sin código extra | Filtrar canceladas en Python |
| Dónde vive la regla | Una función, `servicios.buscar_conflictos` (ADR-009) | La reutiliza la disponibilidad; no puede haber dos versiones de la regla | Repetir la consulta en cada endpoint |
| Respuesta | 409 Conflict con los ids de las reservas que chocan (ADR-010) | El pedido es válido en forma; choca con el estado actual. Los ids ayudan a resolverlo | 422 |
| Concurrencia | Búsqueda de conflictos + `INSERT` dentro de `BEGIN IMMEDIATE` (ADR-011) | Dos pedidos simultáneos en el mismo proceso no pueden pasar ambos la verificación | Verificar fuera de la transacción |

## Criterios de aceptación (pruebas)

1. El ejemplo de la consigna: 10:30–11:30 sobre MIC-01 ocupado de 10:00 a 11:00 → 409
   con el id en conflicto.
2. Seis formas de solapamiento (por el inicio, contenida, que contiene, idéntica, mismo
   inicio, mismo fin) → 409.
3. Una reserva rechazada no queda guardada.
4. Turnos consecutivos en ambos sentidos y hueco exacto entre dos reservas → 201.
5. MIC-02 a la misma hora que MIC-01, y las 5 unidades a la vez → 201.

## Episodios

- **3.1 El ejemplo como prueba:** el escenario de la consigna quedó como fixture
  (`mic01_de_10_a_11`) y sobre él se escribieron las 13 pruebas; 7 en rojo.
- **3.2 Implementación:** `buscar_conflictos` y el error `Conflicto` → 409; 40 pruebas en
  verde.
