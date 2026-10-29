# Progreso del proyecto

Cada fila corresponde a una feature con su propia rama y PR. Estado: ✅ hecho · 🔄 en
curso · ⏳ pendiente. "PR abierto" significa que espera revisión y merge humano.

| # | Feature | Rama | Estado | Pruebas |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Harness del agente y documentación | `feature/harness-agentes` | 🔄 PR #1 abierto | n/a (sin código) |
| 2 | Persistencia SQLite e inventario | `feature/persistencia-inventario` | 🔄 PR #2 abierto | 5/5 ✅ |
| 3 | Crear reserva con validaciones | `feature/crear-reserva` | 🔄 PR #3 abierto | 27/27 ✅ |
| 4 | Reglas de superposición | `feature/reglas-superposicion` | 🔄 PR abierto | 40/40 ✅ |
| 5 | Consulta de disponibilidad | `feature/disponibilidad` | ⏳ | — |
| 6 | Cancelación y persistencia al reiniciar | `feature/cancelacion` | ⏳ | — |
| 7 | README final | `feature/readme` | ⏳ | — |

## Requisitos de prueba de la consigna

Comando: `python -m pytest -v` (Python 3.13.17, pytest 9.2.0).

| Requisito | Prueba | Estado |
| :--- | :--- | :--- |
| Creación válida | `test_crear_reserva.py::test_creacion_valida_devuelve_201_y_reserva_activa` | ✅ |
| Rechazo por superposición | `test_reglas_superposicion.py::test_rechaza_superposicion_del_ejemplo_de_la_consigna` | ✅ |
| Límites consecutivos | `test_reglas_superposicion.py::test_acepta_turno_que_empieza_cuando_termina_otro` | ✅ |
| Unidades distintas simultáneas | `test_reglas_superposicion.py::test_acepta_mic02_en_el_mismo_horario_que_mic01` | ✅ |
| Entradas inválidas (solicitante vacío, inicio ≥ fin, unidad inexistente) | `test_crear_reserva.py::test_rechaza_*` | ✅ |
| Cancelación conserva registro y libera horario | — | ⏳ |
| Persistencia de activas y canceladas tras reiniciar | — | ⏳ |
