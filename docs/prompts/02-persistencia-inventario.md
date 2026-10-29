# Prompt — Feature 2: Persistencia SQLite e inventario

**Rama:** `feature/persistencia-inventario` (sale de `feature/harness-agentes`)

## Contexto suministrado

- `AGENTS.md` (TDD con commits separados, simplicidad, biblioteca estándar primero).
- `Harness/specs.md`, secciones 3 (inventario) y 4.3 (persistencia).
- Plan de features acordado en el hilo del proyecto.

## Instrucción

Extracto de la consigna y la especificación usadas como pedido:

> El sistema debe inicializarse con el siguiente inventario (no se requiere ABM de
> inventario, solo lectura) […] Todos los estados y reservas deben recuperarse
> correctamente al detener y reiniciar la aplicación Uvicorn. […] Proveer un script o
> comando opcional si se requiere reiniciar/limpiar la base de datos, pero la ejecución
> normal no debe borrar datos.

Instrucción operativa del coordinador del proyecto (extracto):

> Begin with init (requirements.txt, structure, SQLite with preloaded inventory), then
> models, endpoints, business logic, tests.

## Episodio 2.1 — Pruebas primero

El agente escribió `tests/test_persistencia_inventario.py` con 5 pruebas: inventario
listado, archivo creado, reinicio sin duplicar ni borrar, script que exige confirmación y
script que borra y recarga. Las commiteó en rojo (todavía no existía `app/`).

## Episodio 2.2 — Implementación mínima

El agente implementó lo mínimo para ponerlas en verde: el esquema con
`CREATE TABLE IF NOT EXISTS`, la carga con `INSERT OR IGNORE`, `crear_app(ruta)` con
inicialización en el `lifespan` de FastAPI y `GET /unidades`.
