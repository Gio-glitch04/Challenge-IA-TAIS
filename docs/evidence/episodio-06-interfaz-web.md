# Episodio 06 — Interfaz web

- **Feature:** 6
- **Rama:** `feature/interfaz-web`
- **Fecha:** 2026-10-29
- **Commits:**
  - `765fc13`, "test: interfaz web servida en / (rojo)"
  - `51d96cb`, "feat: interfaz web en / que usa los mismos endpoints de la API"
  - `415b630`, "refactor: mensajes de error más legibles en la interfaz web"
- **Especificación:** [docs/prompts/06-interfaz-web.md](../prompts/06-interfaz-web.md)
- **Decisiones:** ADR-021 y ADR-022 en [docs/decisions.md](../decisions.md)

## Objetivo y requisito

Que el usuario pueda usar la aplicación desde el navegador: ver el inventario, consultar
disponibilidad, crear, listar y cancelar reservas. Es un complemento de la API; la consigna
no exige interfaz gráfica.

## Verificación ejecutada

### 1. Rojo (commit `765fc13`)

```text
$ python -m pytest -q
3 failed, 72 passed, 1 warning in 2.53s
```

La cuarta prueba nueva (`/` fuera del esquema OpenAPI) ya pasaba antes de la
implementación, porque la ruta todavía no existía.

### 2. Verde (commits `51d96cb` y `415b630`), Python 3.13.17, pytest 9.2.0

```text
$ python -m pytest -q
75 passed, 1 warning in 2.55s
```

### 3. Recorrido en un navegador real

Se levantó la app con `python -m app.main` sobre una base vacía y se recorrió la página
con Chromium (Playwright 1.63.0), completando los formularios como lo haría una persona.
Es una comprobación manual automatizada: el script no forma parte de las pruebas del repo
porque necesita Node y un navegador.

**Resultado esperado:** los casos de la consigna dan el mismo resultado que en la API.
Los mensajes de error son los de la API. Al cancelar, el registro queda como
`cancelada` y el horario se libera.

**Resultado observado:**

```text
inventario: FUE-01 · Fuente de alimentación | MIC-01 · Microscopio digital | MIC-02 · Microscopio digital | MUL-01 · Multímetro | OSC-01 · Osciloscopio
MIC-01 10-11: Reserva creada para MIC-01 (id b0673ec6).
MIC-01 10:30-11:30: 409 · La unidad 'MIC-01' ya está reservada en ese intervalo (reservas: b0673ec6-5579-4b62-8b30-c7e999aaf23d)
MIC-01 11-12: Reserva creada para MIC-01 (id a6d37d21).
MIC-02 10-11: Reserva creada para MIC-02 (id 9b9b9d20).
solicitante vacío: 422 · solicitante: El solicitante no puede estar vacío ni ser solo espacios
inicio > fin: 422 · El inicio debe ser estrictamente anterior al fin
disponibilidad MIC-01 10:15-10:45: MIC-01 está ocupada: Ana Prueba (2030-05-10 10:00:00 a 2030-05-10 11:00:00)
filas: 3
cancelar Ana: Reserva cancelada. El registro se conserva y el horario queda libre.
estado Ana: cancelada
disponibilidad tras cancelar: MIC-01 está libre en ese intervalo.
filtro canceladas: 1
errores JS: Failed to load resource: the server responded with a status of 409 (Conflict); Failed to load resource: the server responded with a status of 422 (Unprocessable Content); Failed to load resource: the server responded with a status of 422 (Unprocessable Content)
```

Los únicos errores de la consola son los registros del navegador de las respuestas 409 y
422 esperadas; no hubo errores de JavaScript. También se revisó la página a 390 px de
ancho (vista de celular).

## Decisión humana

**Pendiente:** revisión y merge del PR de esta feature.
