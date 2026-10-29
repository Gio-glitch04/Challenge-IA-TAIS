# Registro de decisiones

Una sección por feature de la aplicación. Cada decisión (ADR) indica el motivo, la
alternativa descartada cuando hubo una disyuntiva y su consecuencia. Cambiar una decisión ya
acordada requiere aprobación humana (ver `AGENTS.md`, sección 4).

---

## Feature 1 — Persistencia e inventario (`feature/persistencia-inventario`)

**Qué agrega:** `app/database.py` (esquema y carga inicial), `app/inventario.json`,
`app/main.py` con `GET /unidades`, `scripts/reset_db.py` y sus pruebas.

### ADR-001 — SQLite con `sqlite3` de la biblioteca estándar, sin ORM

- **Decisión:** SQL directo con `sqlite3`; una conexión por operación.
- **Motivo:** son dos tablas y tres consultas. Un ORM (SQLAlchemy) sumaría una dependencia
  y una capa que no aporta nada a este tamaño (principio de simplicidad de `AGENTS.md`).
- **Alternativa descartada:** SQLAlchemy + modelos ORM.
- **Consecuencia:** el esquema está en un solo lugar (`ESQUEMA` en `app/database.py`) y
  se lee de un vistazo.

### ADR-002 — Inicialización idempotente y reinicio solo explícito

- **Decisión:** al arrancar, la app ejecuta `CREATE TABLE IF NOT EXISTS` y carga el
  inventario con `INSERT OR IGNORE`. Borrar datos solo es posible con
  `python -m scripts.reset_db --si`; sin `--si` el script no hace nada.
- **Motivo:** la consigna exige que reiniciar Uvicorn no pierda reservas y que el borrado
  sea opcional y explícito.
- **Consecuencia:** la prueba `test_reiniciar_la_app_no_duplica_ni_borra_datos` lo
  verifica. El reinicio con `--si` **borra todas las reservas**.

### ADR-003 — Inventario en un JSON versionado

- **Decisión:** las 5 unidades están en `app/inventario.json` y se cargan al iniciar.
- **Motivo:** el inventario forma parte de la entrega y debe leerse sin abrir la base.
  No hay ABM de inventario (fuera de alcance).

### ADR-004 — Ubicación del archivo de datos

- **Decisión:** por defecto `data/laboratorio.db` (ignorado por Git); se puede cambiar con
  la variable `LAB_DB_PATH`. `crear_app(ruta)` recibe la ruta para que cada prueba use su
  propia base temporal.
- **Consecuencia:** las pruebas nunca tocan la base real.

### Nota sobre dependencias

`fastapi.testclient` muestra un aviso de deprecación que recomienda `httpx2`. Se mantiene
`httpx==0.28.1` porque es la librería que pide la especificación y funciona correctamente;
el aviso no afecta los resultados.


---

## Feature 2 — Crear reserva (`feature/crear-reserva`)

**Qué agrega:** `app/esquemas.py` (modelos Pydantic), `app/servicios.py` (reglas de
negocio), `POST /reservas`, `GET /reservas/{id}` y 27 pruebas en total.

### ADR-005 — Formato de fechas y zona horaria

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

### ADR-006 — Reservas en el pasado y límites de duración

- **Decisión:** se rechaza crear una reserva cuyo **inicio** sea anterior al momento actual
  del servidor. No hay límite de duración máxima ni de anticipación.
- **Motivo:** reservar algo que ya pasó no tiene sentido operativo. La consigna no pide
  límites de duración y agregarlos sería un requisito inventado.
- **Consecuencia:** las pruebas usan fechas de 2030. La consulta de disponibilidad sí
  acepta intervalos pasados (feature 4).

### ADR-007 — Validación en dos capas y códigos HTTP

- **Decisión:** el formato (fechas, solicitante, inicio < fin) lo valida Pydantic en
  `app/esquemas.py`; lo que necesita la base (unidad existente) lo valida
  `app/servicios.py`. Toda entrada inválida responde **422**; una reserva inexistente,
  **404**.
- **Motivo:** la unidad inexistente es un dato inválido del pedido, igual que un
  solicitante vacío, y conviene que el cliente reciba el mismo código.
- **Alternativa descartada:** 404 para unidad inexistente.
- **Consecuencia:** `app/servicios.py` no conoce HTTP; `app/main.py` traduce
  `EntradaInvalida` → 422 y `NoEncontrada` → 404.

### ADR-008 — Identificador y solicitante

- **Decisión:** el id es un UUID4. Al solicitante se le quitan los espacios de los extremos
  y tiene un máximo de 100 caracteres.
- **Motivo:** un UUID no se puede adivinar ni se repite entre reinicios. Guardar el nombre
  sin espacios extremos evita duplicados visuales.
