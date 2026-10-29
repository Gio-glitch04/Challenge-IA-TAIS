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

---

## Feature 3 — Reglas de superposición (`feature/reglas-superposicion`)

**Qué agrega:** `servicios.buscar_conflictos`, el error `Conflicto` (HTTP 409) y 13
pruebas nuevas basadas en el ejemplo de la consigna.

### ADR-009 — Intervalos semiabiertos `[inicio, fin)`

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
  (feature 4), así ambas operaciones aplican exactamente la misma regla.

### ADR-010 — Superposición → 409 Conflict con las reservas en conflicto

- **Decisión:** una superposición responde **409** y el mensaje incluye los ids de las
  reservas que chocan.
- **Motivo:** el pedido es válido en forma (no es un 422); choca con el estado actual del
  recurso. Incluir los ids ayuda a la coordinación a resolverlo.

### ADR-011 — Verificación y alta en la misma transacción

- **Decisión:** `crear_reserva` hace la búsqueda de conflictos y el `INSERT` dentro de
  `BEGIN IMMEDIATE`.
- **Motivo:** SQLite toma el lock de escritura al empezar, así dos pedidos simultáneos en
  el mismo proceso no pueden pasar ambos la verificación. La concurrencia distribuida
  queda fuera de alcance.

---

## Feature 4 — Consulta de disponibilidad (`feature/disponibilidad`)

**Qué agrega:** `GET /unidades/{unidad_id}/disponibilidad?inicio=…&fin=…`, el modelo
`Disponibilidad` y 18 pruebas.

### ADR-012 — Una sola regla para consultar y para reservar

- **Decisión:** la consulta llama a la misma `servicios.buscar_conflictos` que usa la
  creación y valida el intervalo con el mismo modelo `Intervalo` (ISO 8601 sin zona,
  inicio < fin).
- **Motivo:** la consigna exige que la disponibilidad use exactamente las mismas reglas.
  Con una sola función no pueden divergir.
- **Consecuencia:** la prueba parametrizada
  `test_disponibilidad_coincide_con_lo_que_acepta_la_creacion` compara, para 7
  intervalos, la respuesta de la consulta con el resultado real de intentar reservar.

### ADR-013 — Respuesta con los conflictos y 404 para unidad inexistente

- **Decisión:** la respuesta incluye `disponible` y la lista `conflictos` con las reservas
  activas que ocupan el intervalo. Si la unidad no existe responde **404**, porque acá la
  unidad es el recurso de la URL; al crear, la unidad viene en el cuerpo y responde 422
  (ADR-007).
- **Motivo:** saber *quién* ocupa el horario es lo que necesita la coordinación para
  reorganizar.

### ADR-014 — Se puede consultar el pasado

- **Decisión:** a diferencia de la creación (ADR-006), la consulta acepta intervalos
  pasados.
- **Motivo:** consultar no modifica nada y sirve para revisar el historial de uso.

---

## Feature 5 — Cancelación y persistencia al reiniciar (`feature/cancelacion`)

**Qué agrega:** `POST /reservas/{id}/cancelar`, `GET /reservas?unidad_id=&estado=`,
`tests/test_cancelacion.py` y `tests/test_persistencia_reinicio.py`.

### ADR-015 — Cancelar es cambiar el estado, nunca borrar

- **Decisión:** cancelar hace `UPDATE … SET estado = 'cancelada', cancelada_en = <ahora>`.
  No existe ningún endpoint ni función que borre reservas.
- **Motivo:** la consigna exige conservar id y datos. Como la regla de superposición filtra
  por `estado = 'activa'` (ADR-009), el horario queda libre sin ningún código extra.
- **Consecuencia:** el historial completo se puede consultar con `GET /reservas`.

### ADR-016 — Cancelar como `POST /reservas/{id}/cancelar`

- **Decisión:** una acción explícita en lugar de `DELETE /reservas/{id}`.
- **Motivo:** `DELETE` sugiere que el recurso desaparece, y acá se conserva.
- **Alternativa descartada:** `PATCH /reservas/{id}` con `{"estado": "cancelada"}`; abre la
  puerta a otras transiciones de estado que no están en el alcance.

### ADR-017 — Cancelar dos veces → 409

- **Decisión:** cancelar una reserva ya cancelada responde **409** y no modifica
  `cancelada_en`.
- **Motivo:** conserva la fecha de la cancelación original y avisa al cliente de un posible
  doble envío.
- **Supuesto:** se permite cancelar reservas pasadas o en curso; la consigna no lo
  restringe y no afecta a ninguna regla.

### ADR-018 — Verificación de persistencia automática y manual

- **Decisión:** `test_activas_y_canceladas_sobreviven_al_reinicio` arranca y apaga la app
  completa dos veces sobre el mismo archivo. Además, se ejecutó un procedimiento manual con
  Uvicorn real (detener y volver a levantar), documentado con su salida en
  `docs/evidence/episodio-05-cancelacion.md`.

---

## Ajustes posteriores

### ADR-019 — Puerto por defecto 8765 (reemplazado por ADR-020)

- **Decisión:** la API escucha en `127.0.0.1:8765` cuando se levanta con
  `python -m app.main`. La variable `LAB_PORT` cambia el puerto.
- **Motivo:** el autor tenía el 8000, que es el puerto por defecto de Uvicorn, ocupado en su
  máquina. 8765 es poco común y fácil de recordar.
- **Alternativa descartada:** pedir `--port` en cada comando de Uvicorn. Es fácil de
  olvidar y el error ("address already in use") no explica qué hacer.
- **Consecuencia:** el README y `AGENTS.md` usan el 8765. La evidencia del episodio 05
  conserva el 8000 porque registra lo que se ejecutó en ese momento.

### ADR-020 — Puerto por defecto 8800 (reemplaza a ADR-019)

- **Decisión:** el puerto por defecto pasa a ser **8800**. `LAB_PORT` sigue sirviendo para
  cambiarlo.
- **Motivo:** el 8765 también estaba ocupado en la máquina del autor, y el autor eligió el
  8800.
- **Consecuencia:** el README y `AGENTS.md` usan el 8800.
