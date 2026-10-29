# Progreso del proyecto

Cada fila corresponde a una feature de la aplicación, con su propia rama y PR contra `main`.
Estado: ✅ hecho · 🔄 en curso · ⏳ pendiente. "PR abierto" significa que espera revisión y
merge humano.

| # | Feature | Rama | Estado | Pruebas |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Persistencia SQLite e inventario | `feature/persistencia-inventario` | ✅ PR #10 mergeado | 5/5 ✅ |
| 2 | Crear reserva con validaciones | `feature/crear-reserva` | ✅ PR #11 mergeado | 27/27 ✅ |
| 3 | Reglas de superposición | `feature/reglas-superposicion` | ✅ PR #12 mergeado | 40/40 ✅ |
| 4 | Consulta de disponibilidad | `feature/disponibilidad` | ✅ PR #13 mergeado | 58/58 ✅ |
| 5 | Cancelación y persistencia al reiniciar | `feature/cancelacion` | ✅ PR #14 mergeado | 69/69 ✅ |
| 6 | Interfaz web en `/` | `feature/interfaz-web` | 🔄 PR abierto | 75/75 ✅ |

## Requisitos de prueba de la consigna

Comando: `python -m pytest -v` (Python 3.13.17, pytest 9.2.0).

| Requisito | Prueba | Estado |
| :--- | :--- | :--- |
| Creación válida | `test_crear_reserva.py::test_creacion_valida_devuelve_201_y_reserva_activa` | ✅ |
| Rechazo por superposición | `test_reglas_superposicion.py::test_rechaza_superposicion_del_ejemplo_de_la_consigna` | ✅ |
| Límites consecutivos | `test_reglas_superposicion.py::test_acepta_turno_que_empieza_cuando_termina_otro` | ✅ |
| Unidades distintas simultáneas | `test_reglas_superposicion.py::test_acepta_mic02_en_el_mismo_horario_que_mic01` | ✅ |
| Entradas inválidas (solicitante vacío, inicio ≥ fin, unidad inexistente) | `test_crear_reserva.py::test_rechaza_*` | ✅ |
| Cancelación conserva registro y libera horario | `test_cancelacion.py::test_cancelar_conserva_id_y_todos_los_datos`, `::test_cancelar_libera_el_horario_para_una_nueva_reserva` | ✅ |
| Persistencia de activas y canceladas tras reiniciar | `test_persistencia_reinicio.py` + procedimiento manual con Uvicorn (episodio 05) | ✅ |

## Documentación final

| Entregable | Rama | Estado |
| :--- | :--- | :--- |
| README con las 4 secciones de la consigna y 3 episodios | `docs/readme` | ✅ PR #15 mergeado |
| Instalación y guía de uso para Windows al inicio del README | `docs/readme-windows` | ✅ PR #16 mergeado |
| Puerto por defecto 8765 (`LAB_PORT` para cambiarlo), 71/71 ✅ | `fix/puerto-api` | ✅ PR #17 mergeado |
| Puerto por defecto 8800 (el 8765 también estaba ocupado), 71/71 ✅ | `fix/puerto-8800` | ✅ PR #18 mergeado |
