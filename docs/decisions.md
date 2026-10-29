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

### ADR-002 — Una rama y un PR por feature, apilados

- **Decisión:** cada feature va en `feature/<nombre>` con su PR. Como cada una depende de la
  anterior, el PR de la feature N apunta a la rama de la N-1.
- **Motivo:** pedido explícito de separar en el historial la implementación de cada módulo.
  Apilar permite avanzar sin esperar cada merge, que requiere aprobación humana.
- **Alternativa descartada:** que todos los PRs apunten a `main`. Cada PR mostraría también
  los cambios de las features anteriores y la revisión sería confusa.
- **Consecuencia:** los PRs se integran en orden (1 → 2 → …). Al mergear uno, GitHub
  reapunta el siguiente a `main` si se borra la rama integrada.

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

---

## Feature 3 — Crear reserva (`feature/crear-reserva`)

**Qué agrega:** `app/esquemas.py` (modelos Pydantic), `app/servicios.py` (reglas de
negocio), `POST /reservas`, `GET /reservas/{id}` y 27 pruebas en total.

### ADR-008 — Formato de fechas y zona horaria

- **Decisión:** fechas en ISO 8601 **sin zona horaria** (`AAAA-MM-DDTHH:MM[:SS]`),
  interpretadas como hora local del laboratorio. Se rechaza con 422 cualquier fecha con
  offset (`+00:00`, `Z`), con microsegundos, o que no sea texto (por ejemplo un timestamp
  numérico).
- **Motivo:** el laboratorio es un único sitio; mezclar fechas con y sin zona haría
  ambiguas las comparaciones de superposición. Rechazar es más claro que convertir en
  silencio.
- **Alternativa descartada:** normalizar todo a UTC. Obligaría al usuario a pensar en UTC
  para reservar "de 10 a 11".
- **Consecuencia:** las fechas se guardan como texto con formato fijo
  `%Y-%m-%dT%H:%M:%S`, que ordena igual que el tiempo, así SQLite puede comparar
  intervalos como texto.

### ADR-009 — Reservas en el pasado y límites de duración

- **Decisión:** se rechaza crear una reserva cuyo **inicio** sea anterior al momento actual
  del servidor. No hay límite de duración máxima ni de anticipación.
- **Motivo:** reservar algo que ya pasó no tiene sentido operativo. La consigna no pide
  límites de duración y agregarlos sería un requisito inventado.
- **Consecuencia:** las pruebas usan fechas de 2030. La consulta de disponibilidad sí
  acepta intervalos pasados (feature 5).

### ADR-010 — Validación en dos capas y códigos HTTP

- **Decisión:** el formato (fechas, solicitante, inicio < fin) lo valida Pydantic en
  `app/esquemas.py`; lo que necesita la base (unidad existente) lo valida
  `app/servicios.py`. Toda entrada inválida responde **422**; una reserva inexistente,
  **404**.
- **Motivo:** la unidad inexistente es un dato inválido del pedido, igual que un
  solicitante vacío, y conviene que el cliente reciba el mismo código.
- **Alternativa descartada:** 404 para unidad inexistente.
- **Consecuencia:** `app/servicios.py` no conoce HTTP; `app/main.py` traduce
  `EntradaInvalida` → 422 y `NoEncontrada` → 404.

### ADR-011 — Identificador y solicitante

- **Decisión:** el id es un UUID4. Al solicitante se le quitan los espacios de los extremos
  y tiene un máximo de 100 caracteres.
- **Motivo:** un UUID no se puede adivinar ni se repite entre reinicios. Guardar el nombre
  sin espacios extremos evita duplicados visuales.

---

## Feature 4 — Reglas de superposición (`feature/reglas-superposicion`)

**Qué agrega:** `servicios.buscar_conflictos`, el error `Conflicto` (HTTP 409) y 13
pruebas nuevas basadas en el ejemplo de la consigna.

### ADR-012 — Intervalos semiabiertos `[inicio, fin)`

- **Decisión:** dos reservas de la misma unidad chocan si
  `existente.inicio < nueva.fin AND nueva.inicio < existente.fin`, considerando solo
  reservas con `estado = 'activa'`.
- **Motivo:** con desigualdades estrictas, un turno que termina a las 11:00 no choca con
  uno que empieza a las 11:00 (consecutivos permitidos), y cualquier solapamiento real,
  aunque sea de un segundo, se rechaza. Filtrar por `estado = 'activa'` hace que las
  canceladas no bloqueen.
- **Alternativa descartada:** intervalos cerrados `[inicio, fin]`, que rechazarían los
  turnos consecutivos que pide la consigna.
- **Consecuencia:** la misma función se reutiliza en la consulta de disponibilidad
  (feature 5), así ambas operaciones aplican exactamente la misma regla.

### ADR-013 — Superposición → 409 Conflict con las reservas en conflicto

- **Decisión:** una superposición responde **409** y el mensaje incluye los ids de las
  reservas que chocan.
- **Motivo:** el pedido es válido en forma (no es un 422); choca con el estado actual del
  recurso. Incluir los ids ayuda a la coordinación a resolverlo.

### ADR-014 — Verificación y alta en la misma transacción

- **Decisión:** `crear_reserva` hace la búsqueda de conflictos y el `INSERT` dentro de
  `BEGIN IMMEDIATE`.
- **Motivo:** SQLite toma el lock de escritura al empezar, así dos pedidos simultáneos en
  el mismo proceso no pueden pasar ambos la verificación. La concurrencia distribuida
  queda fuera de alcance.
