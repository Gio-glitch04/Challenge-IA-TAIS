# Bitácora de sesiones

Registro cronológico, solo se agregan entradas al final.

## 2026-10-29 — feature/harness-agentes

- Se leyeron la consigna (PDF del challenge) y `Harness/specs.md`.
- Pedido de Giovanni: trabajar en una rama y un PR por feature, documentar cada una en
  `docs/decisions.md`, `docs/prompts/` y `docs/evidence/`, llevar `docs/progress.md` y crear
  `AGENTS.md`.
- Se creó `AGENTS.md` con identidad, memoria local, estrategia de ramas y límites de
  autonomía.
- Se creó el sistema de memoria `.memoria/` (contexto, estado, bitácora).

## 2026-10-29 — feature/persistencia-inventario

- PR #1 (harness) abierto.
- TDD: commit `test:` con 5 pruebas en rojo, después commit `feat:` con la implementación.
- `python -m pytest -v` → 5 passed.
- Prueba manual: `uvicorn app.main:app` + `curl /unidades` devolvió las 5 unidades.
