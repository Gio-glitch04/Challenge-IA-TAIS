# Episodio 04 — Consulta de disponibilidad

- **Feature:** 4
- **Rama:** `feature/disponibilidad`
- **Commits:**
  - `03cbf40`, "test: pruebas de consulta de disponibilidad (rojo)"
  - `a7894dd`, "feat: GET /unidades/{id}/disponibilidad con la misma regla de superposición"
  - `938437a`, "docs: decisiones (ADR-012..014), especificación y progreso de la feature 4"
- **Especificación:** [docs/prompts/04-disponibilidad.md](../prompts/04-disponibilidad.md)
- **Decisiones:** ADR-012 a ADR-014 en [docs/decisions.md](../decisions.md)

## Objetivo y requisito

Consultar disponibilidad por unidad e intervalo con las mismas reglas que la creación.

## Verificación ejecutada

### 1. Rojo (commit `03cbf40`)

```text
$ python -m pytest -q
16 failed, 42 passed, 1 warning in 1.79s
```

### 2. Verde (commit `a7894dd`), Python 3.13.17, pytest 9.2.0

```text
$ python -m pytest -v tests/test_disponibilidad.py
tests/test_disponibilidad.py::test_unidad_sin_reservas_esta_disponible PASSED [  5%]
tests/test_disponibilidad.py::test_intervalo_superpuesto_no_esta_disponible_y_muestra_el_conflicto PASSED [ 11%]
tests/test_disponibilidad.py::test_turno_consecutivo_esta_disponible PASSED [ 16%]
tests/test_disponibilidad.py::test_otra_unidad_en_el_mismo_horario_esta_disponible PASSED [ 22%]
tests/test_disponibilidad.py::test_consultar_no_crea_reservas PASSED     [ 27%]
tests/test_disponibilidad.py::test_disponibilidad_coincide_con_lo_que_acepta_la_creacion[09:00-10:00] PASSED [ 33%]
tests/test_disponibilidad.py::test_disponibilidad_coincide_con_lo_que_acepta_la_creacion[09:30-10:30] PASSED [ 38%]
tests/test_disponibilidad.py::test_disponibilidad_coincide_con_lo_que_acepta_la_creacion[10:00-11:00] PASSED [ 44%]
tests/test_disponibilidad.py::test_disponibilidad_coincide_con_lo_que_acepta_la_creacion[10:15-10:45] PASSED [ 50%]
tests/test_disponibilidad.py::test_disponibilidad_coincide_con_lo_que_acepta_la_creacion[10:59-11:30] PASSED [ 55%]
tests/test_disponibilidad.py::test_disponibilidad_coincide_con_lo_que_acepta_la_creacion[11:00-12:00] PASSED [ 61%]
tests/test_disponibilidad.py::test_disponibilidad_coincide_con_lo_que_acepta_la_creacion[08:00-13:00] PASSED [ 66%]
tests/test_disponibilidad.py::test_unidad_inexistente_devuelve_404 PASSED [ 72%]
tests/test_disponibilidad.py::test_rechaza_inicio_posterior_al_fin PASSED [ 77%]
tests/test_disponibilidad.py::test_rechaza_inicio_igual_al_fin PASSED    [ 83%]
tests/test_disponibilidad.py::test_rechaza_fecha_invalida PASSED         [ 88%]
tests/test_disponibilidad.py::test_rechaza_parametros_faltantes PASSED   [ 94%]
tests/test_disponibilidad.py::test_permite_consultar_intervalos_pasados PASSED [100%]
======================== 18 passed, 1 warning in 0.67s =========================

$ python -m pytest -q
58 passed, 1 warning in 1.96s
```

### 3. Ejemplo de la consigna consultado (TestClient)

```text
POST /reservas MIC-01 10:00-11:00 -> 201
GET /unidades/MIC-01/disponibilidad?inicio=2030-05-10T10:30:00&fin=2030-05-10T11:30:00
-> 200 {"unidad_id": "MIC-01", "inicio": "2030-05-10T10:30:00", "fin": "2030-05-10T11:30:00", "disponible": false, "conflictos": ["0d77b590-3fc9-4112-94f0-45302e10db30"]}
GET /unidades/MIC-01/disponibilidad?inicio=2030-05-10T11:00:00&fin=2030-05-10T12:00:00
-> 200 {"unidad_id": "MIC-01", "inicio": "2030-05-10T11:00:00", "fin": "2030-05-10T12:00:00", "disponible": true, "conflictos": []}
GET /unidades/MIC-02/disponibilidad?inicio=2030-05-10T10:00:00&fin=2030-05-10T11:00:00
-> 200 {"unidad_id": "MIC-02", "inicio": "2030-05-10T10:00:00", "fin": "2030-05-10T11:00:00", "disponible": true, "conflictos": []}
```

## Decisión humana

**Pendiente:** revisión y merge del PR de esta feature.
