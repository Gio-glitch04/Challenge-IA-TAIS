# Registro de decisiones

Una sección por feature/PR. Cada decisión indica el motivo, la alternativa descartada
cuando hubo una disyuntiva y su consecuencia. Cambiar una decisión ya acordada requiere
aprobación humana (ver `AGENTS.md`, sección 4).

---

## Feature 1 — Harness del agente (`feature/harness-agentes`)

**Qué agrega:** `AGENTS.md`, el sistema de memoria local `.memoria/` y la estructura de
documentación `docs/` (progreso, decisiones, prompts y evidencia).

### ADR-001 — Memoria del agente en archivos versionados

- **Decisión:** la memoria del agente vive en `.memoria/` (contexto estable, estado actual
  y bitácora de solo agregado) más `docs/`, todo versionado con Git.
- **Motivo:** la consigna exige conservar progreso y decisiones en un archivo versionado y
  que el repositorio se explique solo. Si la memoria está en Git, cualquier sesión nueva la
  recupera con un `pull` y cada cambio queda trazado en un commit.
- **Alternativa descartada:** solo la memoria propia de la herramienta del agente. No queda
  en el repo y no la puede auditar quien evalúa.
- **Consecuencia:** cada hito lleva un commit `docs:` que actualiza estos archivos.
- **Relación con `Harness/memory.md`:** esa plantilla inicial queda como antecedente; su
  checklist pasa a `docs/progress.md` y sus episodios a `docs/evidence/`.

### ADR-002 — Una rama y un PR contra `main` por feature

- **Decisión:** cada feature va en `feature/<nombre>`, sale de `main` actualizado y se
  integra con su propio PR contra `main`. El PR de la feature siguiente se abre recién
  cuando la anterior ya está mergeada.
- **Motivo:** cada módulo queda separado en el historial y cada merge es una revisión
  humana explícita, que alimenta los episodios de delegación.
- **Alternativa descartada:** PRs apilados (cada uno apuntando a la rama anterior). Se
  probó y se descartó a pedido del responsable: obliga a integrar en cadena y complica la
  revisión independiente de cada feature.
- **Consecuencia:** las features se integran de a una; mientras un PR espera revisión, la
  siguiente puede prepararse localmente.

### ADR-003 — TDD con commits separados

- **Decisión:** para cada regla de negocio se commitea primero la prueba (`test:`) y después
  la implementación (`feat:`).
- **Motivo:** deja evidencia en Git de que la prueba existía y fallaba antes del código.
- **Consecuencia:** el commit `test:` de cada feature puede tener pruebas en rojo; el último
  commit de cada rama siempre queda en verde.

---

## Feature 2 — Persistencia e inventario (`feature/persistencia-inventario`)

**Qué agrega:** `app/database.py` (esquema y carga inicial), `app/inventario.json`,
`app/main.py` con `GET /unidades`, `scripts/reset_db.py` y sus pruebas.

### ADR-004 — SQLite con `sqlite3` de la biblioteca estándar, sin ORM

- **Decisión:** SQL directo con `sqlite3`; una conexión por operación.
- **Motivo:** son dos tablas y tres consultas. Un ORM (SQLAlchemy) sumaría una dependencia
  y una capa que no aporta nada a este tamaño (principio de simplicidad de `AGENTS.md`).
- **Alternativa descartada:** SQLAlchemy + modelos ORM.
- **Consecuencia:** el esquema está en un solo lugar (`ESQUEMA` en `app/database.py`) y
  se lee de un vistazo.

### ADR-005 — Inicialización idempotente y reinicio solo explícito

- **Decisión:** al arrancar, la app ejecuta `CREATE TABLE IF NOT EXISTS` y carga el
  inventario con `INSERT OR IGNORE`. Borrar datos solo es posible con
  `python -m scripts.reset_db --si`; sin `--si` el script no hace nada.
- **Motivo:** la consigna exige que reiniciar Uvicorn no pierda reservas y que el borrado
  sea opcional y explícito.
- **Consecuencia:** la prueba `test_reiniciar_la_app_no_duplica_ni_borra_datos` lo
  verifica. El reinicio con `--si` **borra todas las reservas**.

### ADR-006 — Inventario en un JSON versionado

- **Decisión:** las 5 unidades están en `app/inventario.json` y se cargan al iniciar.
- **Motivo:** el inventario forma parte de la entrega y debe leerse sin abrir la base.
  No hay ABM de inventario (fuera de alcance).

### ADR-007 — Ubicación del archivo de datos

- **Decisión:** por defecto `data/laboratorio.db` (ignorado por Git); se puede cambiar con
  la variable `LAB_DB_PATH`. `crear_app(ruta)` recibe la ruta para que cada prueba use su
  propia base temporal.
- **Consecuencia:** las pruebas nunca tocan la base real.

### Nota sobre dependencias

`fastapi.testclient` muestra un aviso de deprecación que recomienda `httpx2`. Se mantiene
`httpx==0.28.1` porque es la librería que pide la especificación y funciona correctamente;
el aviso no afecta los resultados.
