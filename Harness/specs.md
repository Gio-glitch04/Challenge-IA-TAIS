# Especificación del Sistema de Reservas de Laboratorio

## 1. Contexto y Problema
La coordinación de un laboratorio necesita un sistema para gestionar reservas de equipos. Actualmente sufren de superposiciones de horarios y bloqueos de inventario por cancelaciones mal gestionadas. Se requiere una solución local, pequeña y verificable.

## 2. Stack Tecnológico
*   **Lenguaje:** Python 3.10+
*   **Interfaz:** API Local (FastAPI + Uvicorn)
*   **Persistencia:** SQLite local (archivo `.db`).
*   **Validación de datos:** Pydantic (integrado en FastAPI).
*   **Testing:** Pytest + Httpx.

## 3. Inventario Inicial (Precargado)
El sistema debe inicializarse con el siguiente inventario (no se requiere ABM de inventario, solo lectura):
| ID de unidad | Equipo |
| :--- | :--- |
| MIC-01 | Microscopio digital |
| MIC-02 | Microscopio digital |
| OSC-01 | Osciloscopio |
| MUL-01 | Multímetro |
| FUE-01 | Fuente de alimentación |

## 4. Alcance y Reglas de Negocio

### 4.1 Casos de Uso
1.  **Consultar disponibilidad:** Por unidad y por intervalo de tiempo. Debe respetar las mismas reglas de superposición que la creación.
2.  **Crear reserva:** Requiere unidad (ID), solicitante ficticio, fecha/hora de inicio y fecha/hora de fin. Genera un identificador único de reserva.
3.  **Cancelar reserva:** Se debe conservar en la base de datos con su ID y todos sus datos, pero cambiando su estado a "cancelada". Al cancelar, el intervalo de tiempo vuelve a estar disponible.

### 4.2 Reglas de Validación (Críticas)
*   **Unidad:** Debe existir en el inventario precargado. (Una unidad por reserva es suficiente).
*   **Solicitante:** No puede estar vacío ni compuesto solo por espacios.
*   **Fechas/Horas:** Formato válido (ISO 8601). El inicio debe ser *estrictamente anterior* al fin.
*   **Superposiciones:** RECHAZAR superposiciones de reservas *activas* para la misma unidad.
*   **Límites consecutivos:** PERMITIR reservas consecutivas (ej. fin a las 11:00 e inicio de la siguiente a las 11:00).
*   **Simultaneidad:** PERMITIR reservas en el mismo horario si son para *distintas* unidades (ej. MIC-01 y MIC-02 a la misma hora).
*   **Canceladas:** Una reserva con estado "cancelada" NO bloquea la disponibilidad de ese horario.

### 4.3 Persistencia
*   Todos los estados y reservas deben recuperarse correctamente al detener y reiniciar la aplicación Uvicorn.
*   Advertencia: Proveer un script o comando opcional si se requiere reiniciar/limpiar la base de datos, pero la ejecución normal no debe borrar datos.

## 5. Pruebas Automáticas (Requeridas)
Se deben escribir pruebas con `pytest` que verifiquen explícitamente:
1. Creación válida de reserva.
2. Rechazo por superposición de horarios.
3. Aceptación de límites consecutivos (ej. 10:00-11:00 y 11:00-12:00).
4. Aceptación de unidades distintas simultáneas.
5. Entradas inválidas (solicitante vacío, inicio posterior al fin, unidad inexistente).
6. Cancelación (que conserve el registro en BD pero libere el horario para una nueva reserva).

## 6. Fuera de Alcance
Autenticación, roles, notificaciones, interfaz gráfica, concurrencia distribuida, integraciones externas.