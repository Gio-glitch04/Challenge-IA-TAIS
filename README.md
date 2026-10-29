# Reservas de equipos de laboratorio

API local para consultar disponibilidad, reservar y cancelar unidades de un laboratorio
sin superposiciones y sin perder el historial. La construyó un agente de programación
sobre este repositorio, una feature por vez, y cada entrega pasó por revisión y merge
humano.

- **Versión entregada:** rama `main`.
- **Estado de las pruebas:** `python -m pytest -q` da `71 passed` (Python 3.13.17, pytest 9.2.0).

## Instalación y guía de uso (Windows)

Los comandos son para **PowerShell**. Donde cambia algo en `cmd`, se indica aparte.

### Requisitos

- Python 3.10 o superior, instalado desde [python.org](https://www.python.org/downloads/)
  con la opción *Add python.exe to PATH*. Para comprobarlo: `python --version`.
- Git, para clonar el repositorio. También se puede descargar como ZIP desde GitHub.
- No hace falta ninguna cuenta de un modelo de IA.

### Instalación

```powershell
git clone https://github.com/Gio-glitch04/Challenge-IA-TAIS.git
cd Challenge-IA-TAIS
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

- **En `cmd`:** el entorno se activa con `.venv\Scripts\activate.bat`.
- **Si PowerShell bloquea `Activate.ps1`** con un error de ejecución de scripts,
  habilitalos solo para esa ventana y volvé a activar:

  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\.venv\Scripts\Activate.ps1
  ```

### Ejecutar las pruebas

```powershell
python -m pytest -v
```

Resultado esperado: `71 passed`, con 1 advertencia de deprecación de httpx; ver
[Pendientes y limitaciones](#pendientes-y-limitaciones).

### Levantar la API

```powershell
python -m app.main
```

- **Dirección:** la API queda en `http://127.0.0.1:8765`. Se usa el **8765** y no el 8000
  (el que trae Uvicorn) porque el 8000 suele estar ocupado.
- **Otro puerto:** si el 8765 también está en uso, definí `LAB_PORT` antes de levantar la
  API: `$env:LAB_PORT = "9000"` en PowerShell o `set LAB_PORT=9000` en `cmd`.
- **Con Uvicorn directo:** `python -m uvicorn app.main:app --port 8765` es equivalente.
- **Probar desde el navegador:** abrí `http://127.0.0.1:8765/docs`. Desde ahí se puede
  probar cada endpoint con "Try it out".
- **Detenerla:** con `Ctrl+C`.
- **Datos:** la primera vez se crea `data\laboratorio.db` con el inventario.
- **Reinicios:** detener y volver a levantar la API **no borra** las reservas.

### Guía de uso desde PowerShell

Estos comandos se ejecutan en **otra ventana**, con la API corriendo.

```powershell
# 1. Ver el inventario
Invoke-RestMethod http://127.0.0.1:8765/unidades

# 2. Consultar disponibilidad de MIC-01 entre 10:00 y 11:00
Invoke-RestMethod "http://127.0.0.1:8765/unidades/MIC-01/disponibilidad?inicio=2030-05-10T10:00:00&fin=2030-05-10T11:00:00"

# 3. Crear una reserva (guarda la respuesta en $r)
$cuerpo = @{ unidad_id = "MIC-01"; solicitante = "Ana Prueba"; inicio = "2030-05-10T10:00:00"; fin = "2030-05-10T11:00:00" } | ConvertTo-Json
$r = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8765/reservas -ContentType "application/json" -Body $cuerpo
$r

# 4. Listar reservas (filtros opcionales: unidad_id, estado=activa|cancelada)
Invoke-RestMethod "http://127.0.0.1:8765/reservas?unidad_id=MIC-01"

# 5. Cancelar la reserva creada (se conserva con estado "cancelada")
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8765/reservas/$($r.id)/cancelar"
```

**Cómo se leen las respuestas:**

- **Superposición:** si una reserva choca con otra activa de la misma unidad, la API
  responde **409**.
- **Datos inválidos:** si el solicitante está vacío, las fechas son inválidas o la unidad
  no existe, responde **422**.
- **Cómo verlo en PowerShell:** en esos casos `Invoke-RestMethod` muestra el error en rojo,
  con el mensaje de la API.
- **Formato de las fechas:** ISO 8601 sin zona horaria (`AAAA-MM-DDTHH:MM:SS`), en hora
  local del laboratorio.

### Base de datos: otra ubicación y reinicio

- **Usar otro archivo:** definí la variable `LAB_DB_PATH` antes de levantar la API.

  ```powershell
  $env:LAB_DB_PATH = "data\pruebas.db"      # en cmd: set LAB_DB_PATH=data\pruebas.db
  python -m app.main
  ```

- **Borrar todo:** este comando **BORRA TODAS LAS RESERVAS** y recarga el inventario. Sin
  `--si` no hace nada.

  ```powershell
  python -m scripts.reset_db --si
  ```

| Sección | Contenido |
| :--- | :--- |
| [1. Especificación](#1-especificación) | Problema, alcance, reglas, supuestos y criterios de aceptación |
| [2. Solución](#2-solución) | Estructura, decisiones técnicas, versiones, datos, endpoints, ejemplos y limitaciones |
| [3. Preparación del agente](#3-preparación-del-agente) | Entorno, modelo, instrucciones, contexto, permisos, adaptación y memoria |
| [4. Registro de decisiones y delegación](#4-registro-de-decisiones-y-delegación) | Decisiones significativas y los tres episodios de delegación |

---

## 1. Especificación

La especificación completa está en [`Harness/specs.md`](Harness/specs.md). Se escribió
antes de usar el agente: commit `97541e7`, y un ajuste de nombres en `10494a2`.

### Problema

La coordinación de un laboratorio lleva las reservas en mensajes y en una planilla. Por eso
a veces se confirma la misma unidad en horarios que se pisan, y otras veces una
cancelación sigue bloqueando el horario. Necesita consultar disponibilidad, reservar y
cancelar sin perder el historial.

### Alcance

**Inventario.** El inventario viene precargado y es de solo lectura:

| ID | Equipo |
| :--- | :--- |
| MIC-01, MIC-02 | Microscopio digital |
| OSC-01 | Osciloscopio |
| MUL-01 | Multímetro |
| FUE-01 | Fuente de alimentación |

**Casos de uso:**
1. Consultar la disponibilidad de una unidad en un intervalo.
2. Crear una reserva con unidad, solicitante, inicio y fin. Recibe un id único.
3. Cancelar una reserva. Se conservan el id y los datos, y el estado pasa a `cancelada`.

**Persistencia.** Las reservas y sus estados se recuperan al reiniciar la aplicación.

**Fuera de alcance:** autenticación, roles, notificaciones, interfaz gráfica, pagos,
concurrencia distribuida e integraciones externas.

### Reglas de negocio

| # | Regla | Respuesta si no se cumple |
| :-: | :--- | :--- |
| R1 | La unidad existe en el inventario | 422 al crear, 404 al consultar disponibilidad |
| R2 | El solicitante no está vacío ni es solo espacios | 422 |
| R3 | Las fechas son ISO 8601 válidas y el inicio es estrictamente anterior al fin | 422 |
| R4 | Ninguna otra reserva *activa* de la misma unidad se superpone | 409, con los ids en conflicto |
| R5 | Se permiten turnos consecutivos (uno termina a las 11:00 y otro empieza a las 11:00) | — |
| R6 | Se permite el mismo horario en unidades distintas | — |
| R7 | Una reserva cancelada no bloquea y se conserva en la base | — |
| R8 | La disponibilidad aplica exactamente las reglas R4 a R7 | — |

### Supuestos

Lo que la consigna no especifica se resolvió así. El detalle de cada supuesto está en
[`docs/decisions.md`](docs/decisions.md).

- **Zona horaria y formato.**
  - Las fechas van en ISO 8601 sin zona horaria (`2030-05-10T10:00:00`) y se interpretan
    como hora local del laboratorio. La precisión es de segundos (ADR-005).
  - Se rechazan con 422 las fechas con offset o `Z`, con microsegundos, o que no sean
    texto.
- **Fechas pasadas.** No se puede crear una reserva cuyo inicio ya pasó; la referencia es
  el reloj del servidor (ADR-006). La consulta de disponibilidad sí acepta intervalos
  pasados (ADR-014).
- **Duración y anticipación.** No hay límites de duración ni de anticipación (ADR-006).
- **Intervalos.** Son semiabiertos, `[inicio, fin)`. Dos reservas chocan si
  `inicio_a < fin_b` y `inicio_b < fin_a` (ADR-009).
- **Cancelación.** Cancelar dos veces responde 409 y no cambia la fecha de la primera
  cancelación. Se puede cancelar una reserva pasada o en curso (ADR-017).
- **Solicitante.** Se le quitan los espacios de los extremos y admite hasta 100
  caracteres. Siempre es un nombre ficticio (ADR-008).

### Criterios de aceptación

Cada criterio es una prueba automática que se ejecuta con `python -m pytest -v`. La tabla
completa está en [`docs/progress.md`](docs/progress.md).

| Requisito de la consigna | Prueba |
| :--- | :--- |
| Creación válida | `tests/test_crear_reserva.py::test_creacion_valida_devuelve_201_y_reserva_activa` |
| Rechazo por superposición (MIC-01 10:00–11:00 rechaza 10:30–11:30) | `tests/test_reglas_superposicion.py::test_rechaza_superposicion_del_ejemplo_de_la_consigna` |
| Límites consecutivos (acepta 11:00–12:00) | `tests/test_reglas_superposicion.py::test_acepta_turno_que_empieza_cuando_termina_otro` |
| Unidades distintas simultáneas (MIC-02 10:00–11:00) | `tests/test_reglas_superposicion.py::test_acepta_mic02_en_el_mismo_horario_que_mic01` |
| Entradas inválidas: solicitante vacío, inicio ≥ fin, unidad inexistente | `tests/test_crear_reserva.py::test_rechaza_*` |
| Cancelación que conserva el registro y libera el horario | `tests/test_cancelacion.py::test_cancelar_conserva_id_y_todos_los_datos`, `::test_cancelar_libera_el_horario_para_una_nueva_reserva` |
| La disponibilidad usa las mismas reglas que la creación | `tests/test_disponibilidad.py::test_disponibilidad_coincide_con_lo_que_acepta_la_creacion` |
| Activas y canceladas sobreviven a un reinicio | `tests/test_persistencia_reinicio.py`, más un procedimiento manual con Uvicorn ([episodio 05](docs/evidence/episodio-05-cancelacion.md)) |

### Evolución recuperable en Git

- **Especificación inicial:** `Harness/specs.md` (`97541e7`).
- **Preparación del entorno del agente:** PR #9.
- **Features:** cinco PRs, de #10 a #14, cada uno con un commit `test:` en rojo, un `feat:`
  en verde y la documentación.
- **Decisiones y especificación por feature:** las decisiones de cada feature son una
  sección de [`docs/decisions.md`](docs/decisions.md), y su especificación técnica está en
  [`docs/prompts/`](docs/prompts/).

---

## 2. Solución

### Estructura

```text
app/
  main.py          # FastAPI: rutas y traducción de errores a códigos HTTP
  servicios.py     # reglas de negocio (superposición, crear, cancelar, listar), sin HTTP
  esquemas.py      # modelos Pydantic y validación de fechas, solicitante e intervalo
  database.py      # esquema SQLite e inicialización idempotente
  inventario.json  # inventario inicial (5 unidades)
scripts/reset_db.py  # reinicio explícito de la base (borra reservas)
tests/             # 71 pruebas pytest + httpx (TestClient)
docs/              # decisiones, especificaciones, evidencia y progreso
.memoria/          # memoria de trabajo del agente (contexto, estado, bitácora)
AGENTS.md          # instrucciones del agente (harness)
```

### Decisiones técnicas principales

- **Base de datos:** SQLite con el módulo `sqlite3` de la biblioteca estándar, sin ORM.
  El esquema tiene dos tablas, `unidades` y `reservas`, y la base controla
  `CHECK (inicio < fin)` y `CHECK (estado IN ('activa','cancelada'))`.
- **Regla de superposición en una sola función:** `servicios.buscar_conflictos`. La usan
  tanto la creación como la consulta de disponibilidad.
- **Transacción:** la búsqueda de conflictos y el alta se hacen dentro de la misma
  transacción `BEGIN IMMEDIATE`.
- **Cancelar no borra:** es un `UPDATE` de estado. No existe ningún código que borre
  reservas.

### Requisitos previos y versiones

- Python 3.10 o superior. Se probó con 3.13.17.
- Dependencias fijadas en [`requirements.txt`](requirements.txt): fastapi 0.162.0,
  uvicorn 0.54.0, pydantic 2.14.1, pytest 9.2.0, httpx 0.28.1.
- No hace falta ninguna cuenta de modelo de IA para instalar, ejecutar ni probar.

### Instalación, carga inicial y ejecución

Los comandos para Windows están en [Instalación y guía de uso](#instalación-y-guía-de-uso-windows).

**Carga inicial.** Es automática. Al arrancar, la app crea las tablas si no existen y
carga el inventario con `INSERT OR IGNORE`, así que nunca toca las reservas existentes.

### Dónde persisten los datos y cómo reiniciarlos

- **Ubicación:** los datos se guardan en el archivo `data/laboratorio.db`, que no se
  versiona. Para usar otro archivo, definí la variable `LAB_DB_PATH` (ver la [guía](#base-de-datos-otra-ubicación-y-reinicio)).
- **Reinicio normal:** detener y volver a levantar Uvicorn **no borra nada**.
- **Borrado explícito:** `python -m scripts.reset_db --si` **borra todas las reservas** y
  recarga el inventario. Sin `--si` no hace nada.
- **Pruebas:** cada prueba usa su propio archivo temporal y no toca `data/`.

### Endpoints

| Método y ruta | Uso | Códigos |
| :--- | :--- | :--- |
| `GET /unidades` | Lista el inventario | 200 |
| `GET /unidades/{id}/disponibilidad?inicio=&fin=` | Indica si la unidad está libre y qué reservas la ocupan | 200, 404, 422 |
| `POST /reservas` | Crea una reserva | 201, 409, 422 |
| `GET /reservas?unidad_id=&estado=` | Lista activas y canceladas, con filtros opcionales | 200, 422 |
| `GET /reservas/{id}` | Devuelve una reserva | 200, 404 |
| `POST /reservas/{id}/cancelar` | Cancela una reserva y conserva el registro | 200, 404, 409 |

### Ejemplo de entrada y salida

Se ejecutó el 2026-10-29 contra la app con una base vacía.

```text
POST /reservas {"unidad_id":"MIC-01","solicitante":"Ana Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00"}
201 {"id":"b21ddd20-bd64-42a8-b231-79439b65ee3e","unidad_id":"MIC-01","solicitante":"Ana Prueba","inicio":"2030-05-10T10:00:00","fin":"2030-05-10T11:00:00","estado":"activa","creada_en":"2026-10-29T14:59:01","cancelada_en":null}

POST /reservas {"unidad_id":"MIC-01","solicitante":"Bruno Prueba","inicio":"2030-05-10T10:30:00","fin":"2030-05-10T11:30:00"}
409 {"detail":"La unidad 'MIC-01' ya está reservada en ese intervalo (reservas: b21ddd20-bd64-42a8-b231-79439b65ee3e)"}

GET /unidades/MIC-01/disponibilidad?inicio=2030-05-10T11:00:00&fin=2030-05-10T12:00:00
200 {"unidad_id":"MIC-01","inicio":"2030-05-10T11:00:00","fin":"2030-05-10T12:00:00","disponible":true,"conflictos":[]}

POST /reservas {"unidad_id":"MIC-01","solicitante":"  ","inicio":"2030-05-10T12:00:00","fin":"2030-05-10T11:00:00"}
422 {"detail":[{"type":"value_error","loc":["body","solicitante"],"msg":"Value error, El solicitante no puede estar vacío ni ser solo espacios", ...}]}
```

En [`docs/evidence/episodio-05-cancelacion.md`](docs/evidence/episodio-05-cancelacion.md)
están la cancelación y el reinicio con `curl` y Uvicorn real.

### Pendientes y limitaciones

- **Concurrencia:** está pensada para un solo proceso. `BEGIN IMMEDIATE` evita la doble
  reserva entre pedidos simultáneos sobre el mismo archivo, pero no hay coordinación
  distribuida, que está fuera de alcance.
- **Zona horaria:** no hay soporte. Si el servidor cambia de zona, el control de "inicio en
  el pasado" usa la hora local nueva.
- **Edición:** no se puede editar una reserva ni revertir una cancelación. Para cambiar
  algo, se cancela y se crea otra.
- **Dependencias transitivas:** `requirements.txt` fija solo las dependencias directas; no
  hay un archivo de bloqueo de las transitivas.
- **Advertencia de httpx:** las pruebas muestran 1 advertencia de deprecación, porque
  Starlette sugiere `httpx2` para el `TestClient`. Se mantuvo `httpx` porque la
  especificación lo pide (ver la nota de dependencias en `docs/decisions.md`).

---

## 3. Preparación del agente

### Entorno y modelo

| Dato | Valor | Fuente |
| :--- | :--- | :--- |
| Harness | Claude Code 2.1.312, en la web: un contenedor en la nube dentro de un proyecto de claude.ai | `claude --version` en el contenedor |
| Modelo | `claude-opus-5-5` (configuración de la sesión: `claude-opus-5-5[1m]`) | metadatos de la sesión, campos `model` y `last_served_model` |
| Esfuerzo y permisos | esfuerzo `medium`, modo de permisos `auto` | metadatos de la sesión |
| Python del contenedor | 3.13.17, en un `.venv` | `python --version` |
| Acceso a GitHub | solo este repositorio | configuración de la sesión |

- **Función del agente:** leer la consigna y la especificación, escribir las pruebas y el
  código, ejecutarlos y registrar la evidencia. También abría una rama y un PR por
  feature.
- **Función del autor (Giovanni):** definir la organización del trabajo, revisar cada PR y
  hacer cada merge.
- **Motivo de la elección:** el agente actúa sobre el repositorio con herramientas reales
  (shell, git, pytest, Uvicorn, GitHub), así que se puede verificar lo que ejecutó y no
  solo lo que dijo.
- **Dato no visible:** la versión exacta del contenedor no se muestra.

### Instrucciones y configuración usadas

1. **[`AGENTS.md`](AGENTS.md), en el repositorio (PR #9).**
   - Define el rol del agente y el método: especificación primero y TDD estricto, con un
     commit `test:` en rojo antes del `feat:`.
   - Define los principios de simplicidad, el sistema de memoria y la estrategia de ramas.
   - Define los límites de autonomía (sección 4).
2. **Reglas del autor guardadas en la memoria del proyecto, externa al repositorio.**
   Extracto saneado:
   > El nombre del asistente no debe aparecer en commits, PRs ni nombres de ramas.
   > Cada feature de la aplicación va en su propia rama `feature/<nombre>`, con su PR
   > contra `main`, de a uno, después del merge del anterior. La preparación del entorno
   > no es una feature y va en un PR aparte.

   **Cómo se aplicó:**
   - Las ramas se llaman `feature/*`, `chore/*` y `docs/*`.
   - Los commits los hizo el agente, pero con la identidad de Git del autor.
   - Los PRs no llevan pie de atribución.
   - Los PRs #10 a #14 se abrieron de a uno, cada uno después del merge del anterior.
3. **Plantilla inicial del autor, [`Harness/memory.md`](Harness/memory.md).** La reemplazó
   el sistema de `AGENTS.md` y se conserva como antecedente.

### Contexto suministrado y excluido

- **Suministrado:**
  - el PDF de la consigna, que se compartió en el proyecto y no se versiona;
  - [`Harness/specs.md`](Harness/specs.md);
  - `Harness/memory.md`;
  - los mensajes del autor con la organización del trabajo, resumidos en
    [`docs/prompts/`](docs/prompts/) como especificación técnica, no como transcripción.
- **Excluido:** las conversaciones completas, las credenciales y tokens, el entorno virtual
  y los archivos `.db`, que están en `.gitignore`. Los solicitantes son siempre ficticios
  ("Ana Prueba", "Bruno Prueba").

### Permisos, controles y aprobaciones

- **Lo que el agente podía hacer sin preguntar:**
  - crear ramas y hacer push;
  - ejecutar pruebas, Uvicorn y scripts;
  - editar archivos del repositorio;
  - abrir PRs.
- **Controles previstos.** Según [`AGENTS.md` §4](AGENTS.md), estas acciones requieren al
  autor:
  - hacer merge a `main`;
  - cambiar un ADR acordado;
  - hacer force push o borrar ramas;
  - ejecutar `reset_db` sobre datos reales.

  Además, el modo `auto` del harness revisa cada acción antes de ejecutarla.
- **Controles aplicados:**
  - Los 6 PRs integrados (#9 a #14) los mergeó el autor desde GitHub; el agente no hizo
    ningún merge.
  - Antes de aceptar, el autor revisó en cada PR el diff, la salida de las pruebas en rojo
    y en verde, y los supuestos nuevos.
  - El autor rechazó y cerró la primera organización de PRs (#2 a #8); ver el
    [episodio C](#episodio-c--organización-de-la-entrega-corregido).

### Adaptaciones específicas comprobables

- **Turnos consecutivos.** El ejemplo de la consigna (MIC-01 de 10:00 a 11:00) se
  convirtió en el fixture `mic01_de_10_a_11`, y la regla quedó en una sola función con
  intervalos semiabiertos.
  - **Evidencia:** [episodio 03](docs/evidence/episodio-03-reglas-superposicion.md),
    commits `ceed3c8` (rojo, 7 fallas) y `3c9d020` (verde).
- **Procedimiento de persistencia.** La consigna pide comprobar el reinicio. Se cubrió de
  dos formas: una prueba automática que levanta la app dos veces sobre el mismo archivo, y
  un procedimiento manual con Uvicorn real, con el resultado esperado y el observado.
  - **Evidencia:** [episodio 05](docs/evidence/episodio-05-cancelacion.md).
- **TDD verificable.** `AGENTS.md` obliga a hacer un commit de pruebas en rojo antes de la
  implementación. Cada archivo de evidencia registra la salida en rojo, por ejemplo
  `21 failed, 6 passed` en `825426d`.

### Retención del progreso

El progreso y las decisiones viven en archivos versionados, así que una sesión nueva
retoma el trabajo leyéndolos (protocolo en `AGENTS.md` §2).

| Archivo | Qué guarda |
| :--- | :--- |
| [`.memoria/estado.md`](.memoria/estado.md) | La foto actual del trabajo |
| [`.memoria/bitacora.md`](.memoria/bitacora.md) | El registro cronológico; solo se agregan entradas |
| [`docs/progress.md`](docs/progress.md) | El avance por feature y por prueba |
| [`docs/decisions.md`](docs/decisions.md) | Las decisiones (ADR) |
| [`docs/evidence/`](docs/evidence/) | La evidencia de cada episodio, con sus commits |

### Lo informado por el agente frente a lo ejecutado

Los archivos de evidencia separan dos cosas:

- **Lo ejecutado:** el comando, la versión y la salida copiados de la terminal.
- **Lo descrito:** los resúmenes del agente.

No se omitió ningún paso de verificación. Las salidas en rojo de cada commit `test:` son
las fallas reales que se registraron antes de implementar.

---

## 4. Registro de decisiones y delegación

### Decisiones significativas

El registro completo tiene 19 ADR, con motivo, alternativa y consecuencia, y está en
[`docs/decisions.md`](docs/decisions.md). Estas son las de mayor impacto:

| Decisión | Motivo | Alternativa descartada | Consecuencia |
| :--- | :--- | :--- | :--- |
| SQLite con `sqlite3`, sin ORM (ADR-001) | Dos tablas no justifican otra dependencia | SQLAlchemy | SQL explícito y fácil de revisar |
| Fechas ISO sin zona horaria, en hora local (ADR-005) | Hay un solo laboratorio; mezclar zonas vuelve ambigua la superposición | Normalizar a UTC | Las fechas con offset se rechazan con 422 |
| Unidad inexistente: 422 al crear, 404 al consultar (ADR-007, ADR-013) | Al crear, la unidad es un dato del cuerpo; al consultar, es el recurso de la URL | Usar 404 en ambos | Se documenta la diferencia |
| Intervalo semiabierto `[inicio, fin)` (ADR-009) | Permite turnos consecutivos y rechaza cualquier solapamiento real | Intervalo cerrado | Una sola regla para crear y consultar (ADR-012) |
| Superposición: 409 con los ids en conflicto (ADR-010) | El pedido es válido en forma, pero choca con el estado actual | 422 | El cliente sabe con qué reserva choca |
| Verificar y dar de alta en `BEGIN IMMEDIATE` (ADR-011) | Evita la doble reserva entre pedidos simultáneos | Verificar fuera de la transacción | La concurrencia queda acotada a un solo proceso |
| Cancelar es cambiar el estado, con `POST …/cancelar` (ADR-015, ADR-016) | Conserva el registro; `DELETE` sugiere borrar | `DELETE` o `PATCH` | El historial se puede consultar |

### Tres episodios de delegación

Hubo cinco episodios, uno por feature, documentados en
[`docs/evidence/`](docs/evidence/). Acá se detallan tres: dos sobre reglas críticas y uno
sobre la organización de la entrega, que el autor corrigió.

#### Episodio A — Reglas de superposición (aceptado)

- **Objetivo y requisito:** rechazar superposiciones de reservas activas de la misma
  unidad, permitir turnos consecutivos y permitir unidades distintas en el mismo horario
  (requisitos de prueba 2, 3 y 4; reglas R4 a R6).
- **Contexto e instrucción:**
  - Se le dio `Harness/specs.md` §4.2 y el ejemplo de la consigna.
  - Extracto de la especificación técnica: *"La regla tiene que quedar en un solo lugar,
    porque la consulta de disponibilidad debe aplicar exactamente la misma"*
    ([docs/prompts/03](docs/prompts/03-reglas-superposicion.md)).
- **Acción del agente:**
  - Escribió 13 pruebas: 7 fallaron en rojo y 40 pasaron en verde.
  - Implementó `buscar_conflictos` con intervalos semiabiertos, filtrando solo reservas
    activas.
  - La superposición responde 409 con los ids en conflicto.
  - Registró ADR-009 a ADR-011.
- **Decisión humana:** **aceptado** sin cambios. El autor revisó y mergeó el PR #12
  (`5f7371b`).
- **Evidencia:**
  - [episodio-03](docs/evidence/episodio-03-reglas-superposicion.md);
  - commits `ceed3c8` (rojo) y `3c9d020` (verde);
  - prueba `tests/test_reglas_superposicion.py`.

#### Episodio B — Cancelación y persistencia al reiniciar (aceptado)

- **Objetivo y requisito:**
  - cancelar conservando el id y los datos, y liberar el horario (requisito 6, regla R7);
  - comprobar que las reservas activas y las canceladas sobreviven a un reinicio.
- **Contexto e instrucción:**
  - Se le dio `Harness/specs.md` §4.1 y §4.3, y la consigna.
  - Extracto de la especificación: *"la verificación de persistencia puede ser automática
    o un procedimiento manual reproducible con resultados esperados y observados"*
    ([docs/prompts/05](docs/prompts/05-cancelacion.md)).
- **Acción del agente:**
  - Implementó `POST /reservas/{id}/cancelar` como un `UPDATE` de estado, sin borrar, y
    `GET /reservas` con filtros.
  - Escribió una prueba de reinicio con dos arranques de la app sobre el mismo archivo.
  - Ejecutó el procedimiento manual con Uvicorn y `curl`.
  - El resultado: 10 fallas en rojo y 69 pruebas en verde.
- **Decisión humana:** **aceptado**. El autor revisó y mergeó el PR #14 (`b39b09a`).
- **Evidencia:**
  - [episodio-05](docs/evidence/episodio-05-cancelacion.md);
  - commits `9a54a73` (rojo) y `41de24c` (verde);
  - prueba `tests/test_persistencia_reinicio.py`.

#### Episodio C — Organización de la entrega (corregido)

- **Objetivo y requisito:** que cada parte de la aplicación delegada al agente se pueda
  rastrear por separado. Responde al criterio de trazabilidad de la consigna.
- **Contexto e instrucción:** el autor pidió trabajar por features modulares, cada una con
  su rama, su PR, su sección de decisiones, su especificación y su evidencia.
- **Acción del agente.** La primera propuesta tuvo dos errores:
  - Los PRs #2 a #6 estaban apilados: cada uno salía del anterior.
  - El harness (`AGENTS.md`) contaba como "feature 1" (PRs #1 y #7, y el #8 numerado en
    consecuencia).
- **Decisión humana:** **corregido**. El autor observó que las features debían ser solo
  las de la aplicación, no la preparación del entorno, y que cada PR debía ir contra
  `main`.
  - Cerró los PRs #2 a #6 y #8 sin mergear.
  - Reinició `main` a `10494a2`, de modo que el merge de #1 y #7 no quedó en la historia
    actual.
  - El agente rehízo la entrega así:
    - PR #9 (`chore/preparar-entorno`) para el entorno;
    - PRs #10 a #14, uno por feature contra `main`, cada uno abierto después del merge del
      anterior.

  `AGENTS.md` §2 y §3 incorporan esta regla.
- **Evidencia:**
  - PRs cerrados #2 a #6 y #8 en GitHub, y PR #9;
  - [`AGENTS.md`](AGENTS.md) §3;
  - [`.memoria/bitacora.md`](.memoria/bitacora.md), entrada `chore/preparar-entorno`;
  - la historia lineal de `main` (`git log --oneline main`).
