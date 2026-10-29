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
