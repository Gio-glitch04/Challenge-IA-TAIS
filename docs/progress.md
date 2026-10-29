# Progreso del proyecto

Cada fila corresponde a una feature con su propia rama y PR. Estado: ✅ hecho · 🔄 en
curso · ⏳ pendiente. "PR abierto" significa que espera revisión y merge humano.

| # | Feature | Rama | Estado | Pruebas |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Harness del agente y documentación | `feature/harness-agentes` | 🔄 PR #1 abierto | n/a (sin código) |
| 2 | Persistencia SQLite e inventario | `feature/persistencia-inventario` | 🔄 PR abierto | 5/5 ✅ |
| 3 | Crear reserva con validaciones | `feature/crear-reserva` | ⏳ | — |
| 4 | Reglas de superposición | `feature/reglas-superposicion` | ⏳ | — |
| 5 | Consulta de disponibilidad | `feature/disponibilidad` | ⏳ | — |
| 6 | Cancelación y persistencia al reiniciar | `feature/cancelacion` | ⏳ | — |
| 7 | README final | `feature/readme` | ⏳ | — |

## Requisitos de prueba de la consigna

Comando: `python -m pytest -v` (Python 3.13.17, pytest 9.2.0).

| Requisito | Prueba | Estado |
| :--- | :--- | :--- |
| Creación válida | — | ⏳ |
| Rechazo por superposición | — | ⏳ |
| Límites consecutivos | — | ⏳ |
| Unidades distintas simultáneas | — | ⏳ |
| Entradas inválidas (solicitante vacío, inicio ≥ fin, unidad inexistente) | — | ⏳ |
| Cancelación conserva registro y libera horario | — | ⏳ |
| Persistencia de activas y canceladas tras reiniciar | — | ⏳ |
