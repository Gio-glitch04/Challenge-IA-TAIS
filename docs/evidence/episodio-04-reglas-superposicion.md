# Episodio 04 — Reglas de superposición

- **Rama:** `feature/reglas-superposicion`
- **Commits:**
  - `a4c1b30`, "test: pruebas de superposición, turnos consecutivos y unidades simultáneas (rojo)"
  - `b4ecfbc`, "feat: rechazar superposición de reservas activas de la misma unidad (409)"
  - `3037270`, "docs: decisiones (ADR-012..014), prompt y progreso de la feature 4"
- **Prompt:** [docs/prompts/04-reglas-superposicion.md](../prompts/04-reglas-superposicion.md)
- **Decisiones:** ADR-012 a ADR-014 en [docs/decisions.md](../decisions.md)
- **Adaptación específica del agente:** el ejemplo de turnos consecutivos de la consigna
  quedó como fixture (`mic01_de_10_a_11`) y la regla de intervalos semiabiertos como
  función única reutilizable (`servicios.buscar_conflictos`).

## Objetivo y requisito

Requisitos de prueba 2 (rechazo por superposición), 3 (límites consecutivos) y 4
(unidades distintas simultáneas).

## Verificación ejecutada

### 1. Rojo (commit `a4c1b30`)

```text
$ python -m pytest -q
FAILED tests/test_reglas_superposicion.py::test_rechaza_toda_forma_de_superposicion[10:59-11:00]
7 failed, 33 passed, 1 warning in 1.22s
```

### 2. Verde (commit `b4ecfbc`), Python 3.13.17, pytest 9.2.0

```text
$ python -m pytest -v tests/test_reglas_superposicion.py
tests/test_reglas_superposicion.py::test_rechaza_superposicion_del_ejemplo_de_la_consigna PASSED [  7%]
tests/test_reglas_superposicion.py::test_rechaza_toda_forma_de_superposicion[09:30-10:30] PASSED [ 15%]
tests/test_reglas_superposicion.py::test_rechaza_toda_forma_de_superposicion[10:15-10:45] PASSED [ 23%]
tests/test_reglas_superposicion.py::test_rechaza_toda_forma_de_superposicion[09:00-12:00] PASSED [ 30%]
tests/test_reglas_superposicion.py::test_rechaza_toda_forma_de_superposicion[10:00-11:00] PASSED [ 38%]
tests/test_reglas_superposicion.py::test_rechaza_toda_forma_de_superposicion[10:00-10:01] PASSED [ 46%]
tests/test_reglas_superposicion.py::test_rechaza_toda_forma_de_superposicion[10:59-11:00] PASSED [ 53%]
tests/test_reglas_superposicion.py::test_la_reserva_rechazada_no_se_guarda PASSED [ 61%]
tests/test_reglas_superposicion.py::test_acepta_turno_que_empieza_cuando_termina_otro PASSED [ 69%]
tests/test_reglas_superposicion.py::test_acepta_turno_que_termina_cuando_empieza_otro PASSED [ 76%]
tests/test_reglas_superposicion.py::test_acepta_hueco_exacto_entre_dos_reservas PASSED [ 84%]
tests/test_reglas_superposicion.py::test_acepta_mic02_en_el_mismo_horario_que_mic01 PASSED [ 92%]
tests/test_reglas_superposicion.py::test_acepta_todas_las_unidades_en_el_mismo_horario PASSED [100%]
======================== 13 passed, 1 warning in 0.49s =========================

$ python -m pytest -q
40 passed, 1 warning in 1.41s
```

### 3. El ejemplo de la consigna ejecutado contra la API (TestClient)

```text
MIC-01 10:00-11:00                     -> 201 id=2e482bf9-95d2-4b88-9c04-6e8e17f56685 estado=activa
MIC-01 10:30-11:30 (superpuesta)       -> 409 La unidad 'MIC-01' ya está reservada en ese intervalo (reservas: 2e482bf9-95d2-4b88-9c04-6e8e17f56685)
MIC-01 11:00-12:00 (consecutiva)       -> 201 id=fdfaae2e-6bca-4a00-ad6a-3d29fc0c9752 estado=activa
MIC-02 10:00-11:00 (otra unidad)       -> 201 id=2c307bf7-266a-42be-ad4a-99d5e1a128cd estado=activa
```

## Decisión humana

**Pendiente:** revisión y merge del PR de esta feature por Giovanni.
