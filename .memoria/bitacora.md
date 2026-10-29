# Bitácora de sesiones

Registro cronológico, solo se agregan entradas al final.

## 2026-10-29 — feature/harness-agentes

- Se leyeron la consigna (PDF del challenge) y `Harness/specs.md`.
- Pedido del responsable (Giovanni): una rama y un PR contra `main` por feature,
  documentando cada una en `docs/decisions.md`, `docs/prompts/` y `docs/evidence/`,
  llevar `docs/progress.md` y crear `AGENTS.md`.
- Se creó `AGENTS.md` con identidad, memoria local, estrategia de ramas y límites de
  autonomía.
- Se creó el sistema de memoria `.memoria/` (contexto, estado, bitácora).

## 2026-10-29 — feature/persistencia-inventario

- PR #7 (harness) mergeado por Giovanni (`5f779eb`).
- TDD: commit `test:` con las pruebas en rojo, después commit `feat:` con la implementación.
- `python -m pytest -v` → 5 passed.
- Prueba manual: `uvicorn app.main:app` + `curl /unidades` devolvió las 5 unidades.
