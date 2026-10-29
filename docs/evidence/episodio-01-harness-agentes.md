# Episodio 01 — Harness del agente y memoria local

- **Rama:** `feature/harness-agentes`
- **Commit:** `b274351`, "docs: agregar harness AGENTS.md y sistema de memoria local"
- **Prompt:** [docs/prompts/01-harness-agentes.md](../prompts/01-harness-agentes.md)

## Objetivo y requisito

La consigna pide documentar instrucciones, permisos y controles del agente y conservar
progreso y decisiones en un archivo versionado. Giovanni pidió además un `AGENTS.md`
basado en su plantilla y adaptado a Python.

## Resultado del agente

- `AGENTS.md` con 5 secciones: identidad, memoria local, ramas, límites de autonomía y
  comandos.
- `.memoria/contexto.md`, `.memoria/estado.md` y `.memoria/bitacora.md`.
- `docs/progress.md`, `docs/decisions.md` (ADR-001 a ADR-003) y `docs/prompts/`.

## Verificación ejecutada

Esta feature no tiene código, así que no hay pruebas. Se comprobó que los enlaces internos
de `AGENTS.md` apunten a archivos existentes:

```text
$ for f in Harness/specs.md docs/decisions.md .memoria/contexto.md .memoria/estado.md \
    .memoria/bitacora.md docs/progress.md docs/prompts docs/evidence; do test -e "$f" && echo "ok $f"; done
```

Salida observada:

```text
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

**Aceptado.** Giovanni revisó y mergeó el PR #1 a `main` el 2026-10-29 (merge commit
`73de8e3`, "Merge pull request #1 from Gio-glitch04/feature/harness-agentes"). El agente
no integra a `main` por su cuenta (ver `AGENTS.md`, sección 4).
