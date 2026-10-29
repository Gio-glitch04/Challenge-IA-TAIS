# Episodio 01 — Persistencia SQLite e inventario precargado

- **Feature:** 1
- **Rama:** `feature/persistencia-inventario`
- **Commits:**
  - `92ede01`, "test: pruebas de inventario precargado, persistencia y script de reinicio (rojo)"
  - `2fd4135`, "feat: base SQLite con inventario precargado, GET /unidades y script de reinicio"
  - `2fb16df`, "docs: decisiones, especificación y progreso de la feature 1"
- **Especificación:** [docs/prompts/01-persistencia-inventario.md](../prompts/01-persistencia-inventario.md)
- **Decisiones:** ADR-001 a ADR-004 en [docs/decisions.md](../decisions.md)

## Objetivo y requisito

Inventario de 5 unidades precargado y de solo lectura; persistencia en SQLite que
sobreviva al reinicio; script opcional de limpieza que no se ejecute en el uso normal.

## Verificación ejecutada

### 1. Rojo (commit `92ede01`)

```text
$ python -m pytest -q
tests/conftest.py:4: in <module>
    from app.main import crear_app
E   ModuleNotFoundError: No module named 'app'
```

### 2. Verde (commit `2fd4135`), Python 3.13.17, pytest 9.2.0, fastapi 0.162.0

```text
$ python -m pytest -v
tests/test_persistencia_inventario.py::test_lista_el_inventario_precargado PASSED [ 20%]
tests/test_persistencia_inventario.py::test_crea_el_archivo_sqlite PASSED [ 40%]
tests/test_persistencia_inventario.py::test_reiniciar_la_app_no_duplica_ni_borra_datos PASSED [ 60%]
tests/test_persistencia_inventario.py::test_script_de_reinicio_exige_confirmacion PASSED [ 80%]
tests/test_persistencia_inventario.py::test_script_de_reinicio_borra_reservas_y_recarga_inventario PASSED [100%]
========================= 5 passed, 1 warning in 0.24s =========================
```

### 3. Prueba manual con Uvicorn 0.54.0

```text
$ LAB_DB_PATH=/tmp/manual1.db uvicorn app.main:app --port 8011
$ curl -s localhost:8011/unidades
[{"id":"FUE-01","equipo":"Fuente de alimentación"},{"id":"MIC-01","equipo":"Microscopio digital"},{"id":"MIC-02","equipo":"Microscopio digital"},{"id":"MUL-01","equipo":"Multímetro"},{"id":"OSC-01","equipo":"Osciloscopio"}]
```

## Decisión humana

**Aceptado.** Giovanni revisó y mergeó el PR #10 a `main` el 2026-10-29 (merge commit
`41a4c02`).
