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
