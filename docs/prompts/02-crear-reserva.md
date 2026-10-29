# Especificación técnica — Feature 2: Crear reserva con validaciones

**Rama:** `feature/crear-reserva`

## Qué se pidió (resumen)

Permitir crear una reserva identificable con unidad, solicitante, inicio y fin, y
rechazar toda entrada inválida antes de guardarla. Las reglas que la especificación deja
abiertas (zona horaria, fechas pasadas, límites de duración) se resuelven con supuestos
documentados, sin esperar consultas posteriores.

## Requisitos de entrada

- `Harness/specs.md` §4.1.2 (crear reserva) y §4.2 (validaciones de unidad, solicitante y
  fechas).
- Consigna, "Decisiones y límites técnicos": documentar zona horaria, formato de fechas,
  tratamiento de fechas pasadas y límites de duración o anticipación.
- La superposición queda para la feature 3, así cada PR prueba un grupo de reglas.

## Decisiones y por qué

| Tema | Decisión | Motivo | Alternativa descartada |
| :--- | :--- | :--- | :--- |
| Formato de fechas | ISO 8601 sin zona horaria, hora local del laboratorio, precisión de segundos (ADR-005) | Un solo sitio físico; mezclar fechas con y sin zona haría ambiguas las comparaciones | Normalizar todo a UTC |
| Fechas como texto | Formato fijo `%Y-%m-%dT%H:%M:%S` en SQLite (ADR-005) | Ordena igual que el tiempo, así SQL puede comparar intervalos como texto | Guardar timestamps numéricos |
| Fechas pasadas | Se rechaza crear con inicio anterior al momento actual (ADR-006) | Reservar algo que ya pasó no tiene sentido operativo | Permitirlas |
| Límites de duración | Ninguno (ADR-006) | La consigna no los pide; agregarlos sería un requisito inventado | Máximo de horas por reserva |
| Dónde validar | Formato en Pydantic (`app/esquemas.py`), existencia de la unidad en `app/servicios.py` (ADR-007) | Lo que no necesita base se valida antes de abrir una conexión | Todo en el endpoint |
| Códigos HTTP | Entrada inválida → 422, reserva inexistente → 404 (ADR-007) | Unidad inexistente es un dato inválido del pedido, igual que un solicitante vacío | 404 para unidad inexistente |
| Identificador | UUID4 (ADR-008) | No se puede adivinar ni se repite entre reinicios | Autoincremental |
| Solicitante | Se quitan espacios de los extremos; máximo 100 caracteres (ADR-008) | Evita nombres que solo difieren en espacios | Guardarlo tal cual |
| Atomicidad | Validación y alta dentro de `BEGIN IMMEDIATE` | Prepara el terreno para la verificación de superposición de la feature 3 | Autocommit |

## Criterios de aceptación (pruebas)

1. Creación válida → 201, id, estado `activa`, datos devueltos tal como se guardaron.
2. Cada reserva recibe un id distinto y se puede consultar con `GET /reservas/{id}`.
3. Solicitante vacío, solo espacios o tabulaciones → 422.
4. Inicio posterior o igual al fin → 422.
5. Unidad inexistente → 422 con el id en el mensaje.
6. Fechas no ISO, con zona horaria, en el pasado o campos faltantes → 422.

## Episodios

- **2.1 Pruebas primero:** 21 pruebas nuevas en rojo (las 6 que pasaban eran las de la
  feature 1 y el 404 de una ruta inexistente).
- **2.2 Supuestos:** antes de implementar se fijaron ADR-005 a ADR-008.
- **2.3 Implementación:** modelos, servicio y endpoints; 27 pruebas en verde.
