# Prompt — Feature 1: Harness del agente

**Rama:** `feature/harness-agentes`
**Entorno:** Claude Code en la nube (sesión dentro de un proyecto de claude.ai, con acceso
al repositorio por Git y GitHub).

## Contexto suministrado al agente

- Consigna del challenge (`challenge-agents.pdf`, compartida en el proyecto).
- `Harness/specs.md` y `Harness/memory.md` (ya en el repositorio).
- No se suministraron credenciales ni datos reales.

## Episodio 1.1 — Pedido inicial

Extracto del mensaje de Giovanni:

> Vamos a comenzar con el desarrollo de esto. Guarda en memoria que no debe aparecer tu
> nombre ni en commits, ni en PRs, ni en nombres de branches.

**Qué hizo el agente:** guardó la regla en la memoria del proyecto, configuró el autor
de Git del repositorio con el usuario de GitHub de Giovanni y evitó prefijos con el nombre
del asistente en las ramas. Empezó una rama única con toda la inicialización.

## Episodio 1.2 — Cambio de alcance: modularizar y crear el harness

Extracto del mensaje (editado) de Giovanni:

> Vamos a hacer varios commits/PRs desde branches en el que cada uno se añada una nueva
> feature, todos modularizados […] Por cada PR/feature añadida, hay que agregar una
> respectiva sección que la explique en un archivo llamado decisions.md […] por cada
> feature un archivo markdown (ubicado en /docs/prompts) que explique el prompt usado […]
> un markdown de progreso […] archivos de evidencia en formato md que se encuentren
> separados en episodios […] y especifiquen que commit corresponde a cada uno.
> Es sumamente necesario crear un Harness AGENTS.md […] adaptado a nosotros que usaremos
> python (Cambia algunas palabras para así evitar problemas de copia).

El mensaje incluía la plantilla con cuatro secciones: identidad y filosofía (SDD + TDD,
simplicidad, rebanadas verticales, determinismo, memoria continua), sistema de memoria
local propio, estrategia de ramas y límites de autonomía.

**Qué hizo el agente:**

- Descartó la rama única sin publicarla y reorganizó el trabajo en 7 features apiladas.
- Escribió `AGENTS.md` con redacción propia y lo adaptó a Python: biblioteca estándar
  primero, `pytest`, rutas reales del proyecto y ciclo TDD con commits separados.
- Diseñó la memoria local `.memoria/` (contexto / estado / bitácora) con un protocolo de
  inicio y cierre de sesión.
- Creó `docs/progress.md`, `docs/decisions.md`, `docs/prompts/` y `docs/evidence/`.
