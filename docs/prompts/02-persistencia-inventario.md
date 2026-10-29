# Especificación técnica — Feature 2: Persistencia SQLite e inventario

**Rama:** `feature/persistencia-inventario`

## Qué se pidió (resumen)

Dejar lista la base del sistema: dependencias fijadas, estructura del proyecto, una base
SQLite local con el inventario de 5 unidades precargado y de solo lectura, y una forma
explícita de reiniciar los datos que nunca se ejecute en el uso normal. Empezar por las
pruebas (TDD, según `AGENTS.md`).

## Requisitos de entrada

- `Harness/specs.md` §3 (inventario) y §4.3 (persistencia).
- Consigna: las reservas y sus estados deben recuperarse al reiniciar la aplicación; el
  reinicio de datos debe ser opcional y advertido.

## Decisiones y por qué

| Tema | Decisión | Motivo | Alternativa descartada |
| :--- | :--- | :--- | :--- |
| Acceso a datos | `sqlite3` con SQL directo, una conexión por operación (ADR-004) | Son dos tablas y pocas consultas; un ORM sería una capa sin beneficio | SQLAlchemy |
| Arranque | `CREATE TABLE IF NOT EXISTS` + `INSERT OR IGNORE` en el `lifespan` de FastAPI (ADR-005) | Arrancar N veces deja la base igual: no duplica unidades ni borra reservas | Recrear la base al iniciar |
| Reinicio de datos | `python -m scripts.reset_db --si`; sin `--si` no hace nada (ADR-005) | Borrar datos tiene que ser un acto deliberado | Flag en el arranque de la API |
| Inventario | `app/inventario.json` versionado (ADR-006) | Se lee sin abrir la base y forma parte de la entrega | Inserts hardcodeados en el código |
| Ubicación de datos | `data/laboratorio.db`, configurable con `LAB_DB_PATH`; `crear_app(ruta)` para pruebas (ADR-007) | Cada prueba usa una base temporal y nunca toca la real | Variable global de conexión |
| Restricciones en el esquema | `CHECK (estado IN ('activa','cancelada'))` y `CHECK (inicio < fin)` | La base protege las reglas aunque falle una validación previa | Validar solo en Python |

## Criterios de aceptación (pruebas)

1. `GET /unidades` devuelve exactamente las 5 unidades de la consigna.
2. Al iniciar se crea el archivo SQLite.
3. Reiniciar la app no duplica el inventario ni borra reservas existentes.
4. El script de reinicio sin `--si` no borra nada.
5. El script con `--si` deja 0 reservas y las 5 unidades.

## Episodios

- **2.1 Pruebas primero:** las 5 pruebas se commitearon antes de que existiera `app/`
  (rojo: error de importación).
- **2.2 Implementación mínima:** esquema, carga del inventario, `crear_app` y
  `GET /unidades`, lo justo para pasar a verde.
