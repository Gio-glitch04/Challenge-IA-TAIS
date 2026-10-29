# Especificación técnica — Feature 1: Harness del agente

**Rama:** `feature/harness-agentes`
**Entorno:** Claude Code en la nube, dentro de un proyecto de claude.ai, con acceso al
repositorio por Git y GitHub. El identificador exacto del modelo se documenta en el README
final según lo que muestre la sesión.

## Qué se pidió (resumen)

Antes de escribir código, preparar el entorno de trabajo del agente:

- un `AGENTS.md` que fije el rol, la metodología (SDD + TDD), los principios de trabajo,
  la estrategia de ramas y los límites de autonomía, adaptado a un proyecto Python;
- un sistema de memoria local propio, versionado en el repositorio;
- una estructura de documentación con progreso, decisiones, especificación por módulo y
  evidencia por episodio;
- trabajar en una rama y un PR por feature.

## Contexto que recibió el agente

- La consigna del challenge y `Harness/specs.md`.
- La plantilla inicial `Harness/memory.md`.
- Se excluyeron credenciales y datos reales.

## Decisiones y por qué

| Tema | Decisión | Motivo |
| :--- | :--- | :--- |
| Dónde vive la memoria | `.memoria/` + `docs/`, versionados | La consigna pide progreso y decisiones en archivos versionados; así cualquier sesión nueva los recupera con un `pull` (ADR-001). |
| Estructura de la memoria | Tres archivos: contexto estable, estado actual (se reescribe) y bitácora (solo se agregan entradas) | Separa lo que casi no cambia de lo que cambia en cada sesión y deja un historial que no se pisa. |
| Integración | Una rama `feature/*` y un PR contra `main` por feature, de a uno | Cada módulo queda identificable en el historial y cada merge es una revisión humana (ADR-002). |
| Ciclo de trabajo | Commit `test:` en rojo y después `feat:` en verde | Deja en Git la prueba de que el test existía antes del código (ADR-003). |
| Dependencias | Biblioteca estándar primero (`sqlite3`, `uuid`, `datetime`) | Principio de simplicidad: nada que la especificación no necesite. |
| Autonomía | El agente crea ramas, corre pruebas y abre PRs; merge a `main`, cambios de ADR, force push y borrado de ramas requieren a la persona | Los pasos irreversibles o que cambian lo acordado quedan bajo control humano. |

## Criterios de aceptación

- `AGENTS.md` describe identidad, memoria, ramas, autonomía y comandos.
- Todos los archivos que enlaza `AGENTS.md` existen.
