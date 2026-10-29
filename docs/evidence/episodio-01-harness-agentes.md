# Episodio 01 — Harness del agente y memoria local

- **Rama:** `feature/harness-agentes`
- **Commit:** `1440467`, "docs: agregar harness AGENTS.md y sistema de memoria local"
- **Especificación:** [docs/prompts/01-harness-agentes.md](../prompts/01-harness-agentes.md)
- **Decisiones:** ADR-001 a ADR-003 en [docs/decisions.md](../decisions.md)

## Objetivo y requisito

La consigna pide documentar instrucciones, permisos y controles del agente, y conservar
progreso y decisiones en un archivo versionado.

## Resultado del agente

- `AGENTS.md` con 5 secciones: identidad, memoria local, ramas, límites de autonomía y
  comandos.
- `.memoria/contexto.md`, `.memoria/estado.md` y `.memoria/bitacora.md`.
- `docs/progress.md`, `docs/decisions.md` y `docs/prompts/`.

## Corrección humana durante el episodio

La primera versión integraba las features con PRs apilados. El responsable pidió PRs
independientes contra `main`; se corrigió ADR-002 y la sección 3 de `AGENTS.md`.

## Verificación ejecutada

Esta feature no tiene código, así que no hay pruebas. Se comprobó que existen los archivos
que enlaza `AGENTS.md`:

```text
$ for f in Harness/specs.md docs/decisions.md .memoria/contexto.md .memoria/estado.md \
    .memoria/bitacora.md docs/progress.md docs/prompts docs/evidence; do test -e "$f" && echo "ok $f"; done
ok Harness/specs.md
ok docs/decisions.md
ok .memoria/contexto.md
ok .memoria/estado.md
ok .memoria/bitacora.md
ok docs/progress.md
ok docs/prompts
ok docs/evidence
```

## Decisión humana

**Aceptado.** Giovanni revisó y mergeó el PR #7 a `main` el 2026-10-29 (merge commit
`5f779eb`).
