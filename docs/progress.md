# Progreso del proyecto

Cada fila corresponde a una feature de la aplicación, con su propia rama y PR contra `main`.
Estado: ✅ hecho · 🔄 en curso · ⏳ pendiente. "PR abierto" significa que espera revisión y
merge humano.

| # | Feature | Rama | Estado | Pruebas |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Persistencia SQLite e inventario | `feature/persistencia-inventario` | ⏳ | — |
| 2 | Crear reserva con validaciones | `feature/crear-reserva` | ⏳ | — |
| 3 | Reglas de superposición | `feature/reglas-superposicion` | ⏳ | — |
| 4 | Consulta de disponibilidad | `feature/disponibilidad` | ⏳ | — |
| 5 | Cancelación y persistencia al reiniciar | `feature/cancelacion` | ⏳ | — |

## Requisitos de prueba de la consigna

Comando: `python -m pytest -v`.

| Requisito | Prueba | Estado |
| :--- | :--- | :--- |
| Creación válida | — | ⏳ |
| Rechazo por superposición | — | ⏳ |
| Límites consecutivos | — | ⏳ |
| Unidades distintas simultáneas | — | ⏳ |
| Entradas inválidas (solicitante vacío, inicio ≥ fin, unidad inexistente) | — | ⏳ |
| Cancelación conserva registro y libera horario | — | ⏳ |
| Persistencia de activas y canceladas tras reiniciar | — | ⏳ |
