# AGENTS.md — Harness del agente de programación

Este archivo es el punto de entrada obligatorio para cualquier agente que trabaje en este
repositorio. Se lee completo al iniciar cada sesión, antes de tocar código.

## 1. Identidad y forma de trabajo

- **Rol:** Arquitecto de software senior y responsable técnico del proyecto.
- **Método:** Desarrollo guiado por especificación (SDD) junto con desarrollo guiado por
  pruebas (TDD) estricto.
  - La fuente de verdad funcional es [`Harness/specs.md`](Harness/specs.md). Si algo no está
    especificado, se resuelve con un supuesto razonable y se registra en
    [`docs/decisions.md`](docs/decisions.md) antes de implementarlo.
  - Ciclo TDD por regla de negocio: primero un commit `test:` con la prueba que falla (rojo),
    después el commit `feat:` que la hace pasar (verde), y si hace falta un `refactor:`.

### Principios

- **Simplicidad ante todo:** nada de sobrediseño. Se usa la biblioteca estándar de Python
  (`sqlite3`, `uuid`, `datetime`) siempre que alcance; no se agregan ORMs, capas de
  repositorio vacías ni dependencias que la especificación no pida.
- **Incrementos verticales completos:** cada feature cruza todas las capas que necesita
  (esquema SQLite, lógica en `app/servicios.py`, endpoint FastAPI, pruebas `pytest`) y se
  puede demostrar apenas se termina. No hay interfaz gráfica (fuera de alcance).
- **Resultados deterministas y verificables:** una tarea está terminada solo si
  `python -m pytest` pasa en verde y la evidencia (comando, versión, salida) quedó en
  `docs/evidence/`. Lo que el agente *dice* que hizo se distingue siempre de lo que se
  *ejecutó* realmente.
- **Memoria continua:** el progreso y las decisiones viven en archivos versionados del
  repositorio (sección 2), nunca solo en la conversación.

## 2. Sistema de memoria local

La memoria del agente es un conjunto pequeño de archivos Markdown versionados con Git.
Al estar en el repo, cualquier sesión nueva (o una persona) recupera el estado con un
`git pull`, y la historia de cada cambio queda auditada en los commits.

| Archivo | Qué guarda | Cómo se escribe |
| :--- | :--- | :--- |
| [`.memoria/contexto.md`](.memoria/contexto.md) | Hechos estables: stack, inventario, reglas críticas, convenciones, rutas clave. | Se edita solo si cambia un hecho acordado. |
| [`.memoria/estado.md`](.memoria/estado.md) | Foto del momento: rama activa, último paso hecho, próximo paso, bloqueos. | Se **reescribe** al cerrar cada sesión o hito. |
| [`.memoria/bitacora.md`](.memoria/bitacora.md) | Registro cronológico de sesiones y acciones. | **Solo se agregan** entradas al final; nunca se borran. |
| [`docs/progress.md`](docs/progress.md) | Avance por feature y resultado de las pruebas. | Se actualiza en cada PR. |
| [`docs/decisions.md`](docs/decisions.md) | Decisiones técnicas (ADR) y supuestos, una sección por feature. | Se agrega una sección por PR. |
| [`docs/prompts/`](docs/prompts/) | Especificación técnica de cada módulo: qué se pidió, qué se decidió y por qué. | Un archivo por feature. |
| [`docs/evidence/`](docs/evidence/) | Evidencia por episodio: commits, comandos ejecutados, salida, revisión humana. | Un archivo por episodio. |

Las features son solo las de la aplicación. La preparación del entorno (este archivo,
`.memoria/` y el esqueleto de `docs/`) no cuenta como feature ni genera entradas en
`decisions.md`, `prompts/` o `evidence/`.

### Protocolo de sesión

1. **Al empezar:** leer `AGENTS.md` → `.memoria/contexto.md` → `.memoria/estado.md` →
   `docs/progress.md`. Ejecutar `python -m pytest` para confirmar que el punto de partida
   está en verde.
2. **Durante:** cada decisión no trivial se anota en `docs/decisions.md` *antes* del commit
   que la implementa.
3. **Al cerrar un hito o una sesión:** agregar una entrada a `.memoria/bitacora.md`,
   reescribir `.memoria/estado.md`, actualizar `docs/progress.md` y crear o completar el
   archivo de evidencia del episodio con el hash del commit.
4. No se guardan secretos, tokens, credenciales ni datos personales reales en la memoria.
   Los solicitantes de ejemplo son siempre ficticios.

## 3. Ramas y orquestación de agentes

- **Rama base:** `main`.
- **Una feature, una rama:** cada feature de la aplicación se desarrolla aislada en
  `feature/<nombre>`,
  sale de `main` actualizado y se integra mediante su propio Pull Request contra `main`.
- Los PRs se abren de a uno: el de la feature siguiente se abre cuando la anterior ya está
  en `main`.
- Los cambios que no son features (entorno, configuración, documentación general) van en
  ramas `chore/<nombre>` o `docs/<nombre>`, también con PR contra `main`.
- Si se usan subagentes, cada uno trabaja en su propia rama o en un worktree dedicado; nunca
  dos agentes escriben en la misma rama a la vez.
- **Antes de integrar** cualquier rama a `main`, las pruebas automáticas deben pasar.
- **Commits semánticos y atómicos:** `feat:`, `fix:`, `test:`, `docs:`, `refactor:`,
  `chore:`. Un commit = un cambio con sentido propio.
- Los nombres de ramas, commits y PRs no incluyen el nombre del asistente ni pies de
  atribución automáticos.

## 4. Límites de autonomía y aprobación humana

**El agente puede hacer sin preguntar:**

- Crear ramas `feature/*` y hacer push de ellas.
- Ejecutar pruebas, el servidor local y scripts del proyecto.
- Leer y escribir archivos dentro del espacio de trabajo del repositorio.
- Abrir Pull Requests.

**Requiere confirmación explícita de la persona responsable:**

- Cambiar una decisión de arquitectura ya acordada (cualquier ADR de `docs/decisions.md`).
- Hacer merge a `main`.
- `git push --force`, reescribir historia publicada o borrar ramas.
- Ejecutar `scripts/reset_db.py` sobre una base con datos que no sean de prueba.

## 5. Comandos del proyecto

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -v                       # pruebas
uvicorn app.main:app --reload             # API local en http://127.0.0.1:8000/docs
```
