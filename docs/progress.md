# Progreso del proyecto

Cada fila corresponde a una feature de la aplicación, con su propia rama y PR contra `main`.
Estado: ✅ hecho · 🔄 en curso · ⏳ pendiente. "PR abierto" significa que espera revisión y
merge humano.

| # | Feature | Rama | Estado | Pruebas |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Persistencia SQLite e inventario | `feature/persistencia-inventario` | ✅ PR #10 mergeado | 5/5 ✅ |
| 2 | Crear reserva con validaciones | `feature/crear-reserva` | ✅ PR #11 mergeado | 27/27 ✅ |
| 3 | Reglas de superposición | `feature/reglas-superposicion` | ✅ PR #12 mergeado | 40/40 ✅ |
| 4 | Consulta de disponibilidad | `feature/disponibilidad` | 🔄 PR abierto | 58/58 ✅ |
| 5 | Cancelación y persistencia al reiniciar | `feature/cancelacion` | ⏳ | — |

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
