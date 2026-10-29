# Episodio 03 — Crear reserva con validaciones

- **Rama:** `feature/crear-reserva`
- **Commits:**
  - `3d82ca0`, "test: pruebas de creación válida y entradas inválidas de reservas (rojo)"
  - `986f9eb`, "feat: POST /reservas y GET /reservas/{id} con validación de unidad, solicitante y fechas"
  - `33c21fc`, "docs: decisiones (ADR-008..011), prompt y progreso de la feature 3"
- **Prompt:** [docs/prompts/03-crear-reserva.md](../prompts/03-crear-reserva.md)
- **Decisiones:** ADR-008 a ADR-011 en [docs/decisions.md](../decisions.md)

## Objetivo y requisito

Requisitos de prueba 1 (creación válida) y 5 (entradas inválidas: solicitante vacío,
inicio posterior al fin, unidad inexistente) de la especificación.

## Verificación ejecutada

### 1. Rojo (commit `3d82ca0`)

```text
$ python -m pytest -q
FAILED tests/test_crear_reserva.py::test_rechaza_campos_faltantes[inicio] - A...
FAILED tests/test_crear_reserva.py::test_rechaza_campos_faltantes[fin] - Asse...
21 failed, 6 passed, 1 warning in 0.82s
```

### 2. Verde (commit `986f9eb`), Python 3.13.17, pytest 9.2.0

```text
$ python -m pytest -v
tests/test_crear_reserva.py::test_creacion_valida_devuelve_201_y_reserva_activa PASSED [  3%]
tests/test_crear_reserva.py::test_cada_reserva_tiene_un_id_unico PASSED  [  7%]
tests/test_crear_reserva.py::test_la_reserva_creada_se_puede_consultar_por_id PASSED [ 11%]
tests/test_crear_reserva.py::test_consultar_reserva_inexistente_devuelve_404 PASSED [ 14%]
tests/test_crear_reserva.py::test_el_solicitante_se_guarda_sin_espacios_extremos PASSED [ 18%]
tests/test_crear_reserva.py::test_rechaza_solicitante_vacio_o_solo_espacios[] PASSED [ 22%]
tests/test_crear_reserva.py::test_rechaza_solicitante_vacio_o_solo_espacios[   ] PASSED [ 25%]
tests/test_crear_reserva.py::test_rechaza_solicitante_vacio_o_solo_espacios[\t\n] PASSED [ 29%]
tests/test_crear_reserva.py::test_rechaza_inicio_posterior_al_fin PASSED [ 33%]
tests/test_crear_reserva.py::test_rechaza_inicio_igual_al_fin PASSED     [ 37%]
tests/test_crear_reserva.py::test_rechaza_unidad_inexistente PASSED      [ 40%]
tests/test_crear_reserva.py::test_rechaza_fechas_que_no_son_iso_8601[10/05/2030 10:00] PASSED [ 44%]
tests/test_crear_reserva.py::test_rechaza_fechas_que_no_son_iso_8601[2030-13-01T10:00:00] PASSED [ 48%]
tests/test_crear_reserva.py::test_rechaza_fechas_que_no_son_iso_8601[ma\xf1ana] PASSED [ 51%]
tests/test_crear_reserva.py::test_rechaza_fechas_que_no_son_iso_8601[] PASSED [ 55%]
tests/test_crear_reserva.py::test_rechaza_fechas_que_no_son_iso_8601[1893456000] PASSED [ 59%]
tests/test_crear_reserva.py::test_rechaza_fechas_con_zona_horaria PASSED [ 62%]
tests/test_crear_reserva.py::test_rechaza_reservas_que_empiezan_en_el_pasado PASSED [ 66%]
tests/test_crear_reserva.py::test_rechaza_campos_faltantes[unidad_id] PASSED [ 70%]
tests/test_crear_reserva.py::test_rechaza_campos_faltantes[solicitante] PASSED [ 74%]
tests/test_crear_reserva.py::test_rechaza_campos_faltantes[inicio] PASSED [ 77%]
tests/test_crear_reserva.py::test_rechaza_campos_faltantes[fin] PASSED   [ 81%]
tests/test_persistencia_inventario.py::test_lista_el_inventario_precargado PASSED [ 85%]
tests/test_persistencia_inventario.py::test_crea_el_archivo_sqlite PASSED [ 88%]
tests/test_persistencia_inventario.py::test_reiniciar_la_app_no_duplica_ni_borra_datos PASSED [ 92%]
tests/test_persistencia_inventario.py::test_script_de_reinicio_exige_confirmacion PASSED [ 96%]
tests/test_persistencia_inventario.py::test_script_de_reinicio_borra_reservas_y_recarga_inventario PASSED [100%]
======================== 27 passed, 1 warning in 0.92s =========================
```

### 3. Ejemplo de entrada y salida (TestClient con base temporal)

```text
POST /reservas {"unidad_id": "MIC-01", "solicitante": "Ana Prueba", "inicio": "2030-05-10T10:00:00", "fin": "2030-05-10T11:00:00"}
-> 201 {"id": "3c0e1906-74a5-40ed-84ac-961a32661515", "unidad_id": "MIC-01", "solicitante": "Ana Prueba", "inicio": "2030-05-10T10:00:00", "fin": "2030-05-10T11:00:00", "estado": "activa", "creada_en": "2026-10-29T13:02:36", "cancelada_en": null}

POST /reservas {"unidad_id": "MIC-01", "solicitante": "   ", "inicio": "2030-05-10T10:00:00", "fin": "2030-05-10T11:00:00"}
-> 422 {"detail": ["Value error, El solicitante no puede estar vacío ni ser solo espacios"]}

POST /reservas {"unidad_id": "XYZ-99", "solicitante": "Ana Prueba", "inicio": "2030-05-10T10:00:00", "fin": "2030-05-10T11:00:00"}
-> 422 {"detail": "La unidad 'XYZ-99' no existe en el inventario"}

POST /reservas {"unidad_id": "MIC-01", "solicitante": "Ana Prueba", "inicio": "2030-05-10T12:00:00", "fin": "2030-05-10T11:00:00"}
-> 422 {"detail": ["Value error, El inicio debe ser estrictamente anterior al fin"]}
```

## Decisión humana

**Pendiente:** Giovanni revisa los supuestos ADR-008 a ADR-011 y el PR de esta feature.
Si cambia alguno (por ejemplo, permitir reservas en el pasado), se registra acá.
