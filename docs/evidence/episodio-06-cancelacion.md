# Episodio 06 — Cancelación y persistencia al reiniciar

- **Rama:** `feature/cancelacion`
- **Commits:**
  - `c91fb57`, "test: pruebas de cancelación, listado y persistencia al reiniciar (rojo)"
  - `34d2768`, "feat: POST /reservas/{id}/cancelar y GET /reservas con filtros; la cancelación conserva el registro"
  - `b96648b`, "docs: decisiones (ADR-018..021), prompt y progreso de la feature 6"
- **Prompt:** [docs/prompts/06-cancelacion.md](../prompts/06-cancelacion.md)
- **Decisiones:** ADR-018 a ADR-021 en [docs/decisions.md](../decisions.md)

## Objetivo y requisito

Requisito de prueba 6 (cancelación que conserva el registro y libera el horario) y
verificación de persistencia de activas y canceladas tras reiniciar.

## Verificación ejecutada

### 1. Rojo (commit `c91fb57`)

```text
$ python -m pytest -q
10 failed, 59 passed, 1 warning in 2.61s
```

### 2. Verde (commit `34d2768`), Python 3.13.17, pytest 9.2.0

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
======================== 11 passed, 1 warning in 0.56s =========================

$ python -m pytest -q
69 passed, 1 warning in 2.90s
```

### 3. Procedimiento manual reproducible: detener y reiniciar Uvicorn

**Resultado esperado:** después de reiniciar, `GET /reservas` devuelve las dos reservas;
MIC-01 en `activa` y MIC-02 en `cancelada`, con los mismos ids y datos.

**Resultado observado** (uvicorn 0.54.0, 2026-10-29):

```text
$ export LAB_DB_PATH=data/manual-reinicio.db
$ uvicorn app.main:app --port 8000   # 1ª ejecución
$ curl -s -X POST localhost:8000/reservas -H "Content-Type: application/json" -d '{"unidad_id":"MIC-01","solicitante":"Ana Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00"}'
{"id":"3b7938f1-3493-4b84-ae09-d47f9890d57b","unidad_id":"MIC-01","solicitante":"Ana Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"activa","creada_en":"2026-10-29T13:07:44","cancelada_en":null}
$ curl -s -X POST localhost:8000/reservas -H "Content-Type: application/json" -d '{"unidad_id":"MIC-02","solicitante":"Bruno Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00"}'
{"id":"96d2a3a7-134e-46ef-b733-7b695de7a044","unidad_id":"MIC-02","solicitante":"Bruno Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"activa","creada_en":"2026-10-29T13:07:44","cancelada_en":null}
$ curl -s -X POST localhost:8000/reservas/<id de MIC-02>/cancelar
{"id":"96d2a3a7-134e-46ef-b733-7b695de7a044","unidad_id":"MIC-02","solicitante":"Bruno Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"cancelada","creada_en":"2026-10-29T13:07:44","cancelada_en":"2026-10-29T13:07:44"}
$ # Ctrl+C: se detiene Uvicorn
$ uvicorn app.main:app --port 8000   # 2ª ejecución, mismo archivo
$ curl -s localhost:8000/reservas
[{"id":"3b7938f1-3493-4b84-ae09-d47f9890d57b","unidad_id":"MIC-01","solicitante":"Ana Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"activa","creada_en":"2026-10-29T13:07:44","cancelada_en":null},{"id":"96d2a3a7-134e-46ef-b733-7b695de7a044","unidad_id":"MIC-02","solicitante":"Bruno Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"cancelada","creada_en":"2026-10-29T13:07:44","cancelada_en":"2026-10-29T13:07:44"}]
```

Coincide con lo esperado. El archivo `data/manual-reinicio.db` se borró al terminar
(no se versiona).

## Decisión humana

**Pendiente:** revisión y merge del PR de esta feature por Giovanni.
