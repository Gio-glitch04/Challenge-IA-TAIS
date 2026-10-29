# Episodio 05 — Cancelación y persistencia al reiniciar

- **Feature:** 5
- **Rama:** `feature/cancelacion`
- **Commits:**
  - `9a54a73`, "test: pruebas de cancelación, listado y persistencia al reiniciar (rojo)"
  - `41de24c`, "feat: POST /reservas/{id}/cancelar y GET /reservas con filtros; la cancelación conserva el registro"
  - `b495ef7`, "docs: decisiones (ADR-015..018), especificación y progreso de la feature 5"
- **Especificación:** [docs/prompts/05-cancelacion.md](../prompts/05-cancelacion.md)
- **Decisiones:** ADR-015 a ADR-018 en [docs/decisions.md](../decisions.md)

## Objetivo y requisito

Requisito de prueba 6 (cancelación que conserva el registro y libera el horario) y
verificación de persistencia de activas y canceladas tras reiniciar.

## Verificación ejecutada

### 1. Rojo (commit `9a54a73`)

```text
$ python -m pytest -q
10 failed, 59 passed, 1 warning in 2.52s
```

### 2. Verde (commit `41de24c`), Python 3.13.17, pytest 9.2.0

```text
$ python -m pytest -v tests/test_cancelacion.py tests/test_persistencia_reinicio.py
tests/test_cancelacion.py::test_cancelar_devuelve_la_reserva_con_estado_cancelada PASSED [  9%]
tests/test_cancelacion.py::test_cancelar_conserva_id_y_todos_los_datos PASSED [ 18%]
tests/test_cancelacion.py::test_cancelar_conserva_la_fila_en_la_base PASSED [ 27%]
tests/test_cancelacion.py::test_cancelar_libera_el_horario_para_una_nueva_reserva PASSED [ 36%]
tests/test_cancelacion.py::test_la_reserva_cancelada_no_bloquea_la_disponibilidad PASSED [ 45%]
tests/test_cancelacion.py::test_cancelar_dos_veces_devuelve_409 PASSED   [ 54%]
tests/test_cancelacion.py::test_cancelar_reserva_inexistente_devuelve_404 PASSED [ 63%]
tests/test_cancelacion.py::test_listado_incluye_activas_y_canceladas PASSED [ 72%]
tests/test_cancelacion.py::test_listado_filtra_por_unidad_y_estado PASSED [ 81%]
tests/test_cancelacion.py::test_listado_rechaza_estado_desconocido PASSED [ 90%]
tests/test_persistencia_reinicio.py::test_activas_y_canceladas_sobreviven_al_reinicio PASSED [100%]
======================== 11 passed, 1 warning in 0.57s =========================

$ python -m pytest -q
69 passed, 1 warning in 3.00s
```

### 3. Procedimiento manual reproducible: detener y reiniciar Uvicorn

**Resultado esperado:** después de reiniciar, `GET /reservas` devuelve las dos reservas,
MIC-01 en `activa` y MIC-02 en `cancelada`, con los mismos ids y datos.

**Resultado observado** (uvicorn 0.54.0, 2026-10-29):

```text
$ export LAB_DB_PATH=data/manual-reinicio.db
$ uvicorn app.main:app --port 8000   # 1ª ejecución
$ curl -s -X POST localhost:8000/reservas -H "Content-Type: application/json" -d '{"unidad_id":"MIC-01","solicitante":"Ana Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00"}'
{"id":"8e695ee2-59c7-4a88-a404-0071243b6c56","unidad_id":"MIC-01","solicitante":"Ana Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"activa","creada_en":"2026-10-29T14:32:00","cancelada_en":null}
$ curl -s -X POST localhost:8000/reservas -H "Content-Type: application/json" -d '{"unidad_id":"MIC-02","solicitante":"Bruno Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00"}'
{"id":"e6ec5909-c898-471a-993c-55345de78468","unidad_id":"MIC-02","solicitante":"Bruno Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"activa","creada_en":"2026-10-29T14:32:00","cancelada_en":null}
$ curl -s -X POST localhost:8000/reservas/<id de MIC-02>/cancelar
{"id":"e6ec5909-c898-471a-993c-55345de78468","unidad_id":"MIC-02","solicitante":"Bruno Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"cancelada","creada_en":"2026-10-29T14:32:00","cancelada_en":"2026-10-29T14:32:00"}
$ # Ctrl+C: se detiene Uvicorn
$ uvicorn app.main:app --port 8000   # 2ª ejecución, mismo archivo
$ curl -s localhost:8000/reservas
[{"id":"8e695ee2-59c7-4a88-a404-0071243b6c56","unidad_id":"MIC-01","solicitante":"Ana Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"activa","creada_en":"2026-10-29T14:32:00","cancelada_en":null},{"id":"e6ec5909-c898-471a-993c-55345de78468","unidad_id":"MIC-02","solicitante":"Bruno Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"cancelada","creada_en":"2026-10-29T14:32:00","cancelada_en":"2026-10-29T14:32:00"}]
```

Coincide con lo esperado. El archivo `data/manual-reinicio.db` se borró al terminar
(no se versiona).

## Decisión humana

**Aceptado.** Giovanni revisó y mergeó el PR #14 a `main` el 2026-10-29 (merge commit
`b39b09a`).
