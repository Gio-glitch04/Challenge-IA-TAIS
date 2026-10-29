# Episodio 02 — Persistencia SQLite e inventario precargado

- **Rama:** `feature/persistencia-inventario`
- **Commits:**
  - `2290b1e`, "test: pruebas de inventario precargado, persistencia y script de reinicio (rojo)"
  - `5f31ea6`, "feat: base SQLite con inventario precargado, GET /unidades y script de reinicio"
  - `305a75f`, "docs: decisiones, especificación y progreso de la feature 2"
- **Especificación:** [docs/prompts/02-persistencia-inventario.md](../prompts/02-persistencia-inventario.md)
- **Decisiones:** ADR-004 a ADR-007 en [docs/decisions.md](../decisions.md)

## Objetivo y requisito

Inventario de 5 unidades precargado y de solo lectura; persistencia en SQLite que
sobreviva al reinicio; script opcional de limpieza que no se ejecute en el uso normal.

## Verificación ejecutada

### 1. Rojo (commit `2290b1e`)

```text
$ python -m pytest -q
tests/conftest.py:4: in <module>
    from app.main import crear_app
E   ModuleNotFoundError: No module named 'app'
```

### 2. Verde (commit `5f31ea6`), Python 3.13.17, pytest 9.2.0, fastapi 0.162.0

```text
$ python -m pytest -v
tests/test_persistencia_inventario.py::test_lista_el_inventario_precargado PASSED [ 20%]
tests/test_persistencia_inventario.py::test_crea_el_archivo_sqlite PASSED [ 40%]
tests/test_persistencia_inventario.py::test_reiniciar_la_app_no_duplica_ni_borra_datos PASSED [ 60%]
tests/test_persistencia_inventario.py::test_script_de_reinicio_exige_confirmacion PASSED [ 80%]
tests/test_persistencia_inventario.py::test_script_de_reinicio_borra_reservas_y_recarga_inventario PASSED [100%]
========================= 5 passed, 1 warning in 0.35s =========================
```

### 3. Prueba manual con Uvicorn 0.54.0

```text
$ LAB_DB_PATH=/tmp/manual2.db uvicorn app.main:app --port 8011
$ curl -s localhost:8011/unidades
[{"id":"FUE-01","equipo":"Fuente de alimentación"},{"id":"MIC-01","equipo":"Microscopio digital"},{"id":"MIC-02","equipo":"Microscopio digital"},{"id":"MUL-01","equipo":"Multímetro"},{"id":"OSC-01","equipo":"Osciloscopio"}]
```

## Decisión humana

**Pendiente:** revisión y merge del PR de esta feature.
