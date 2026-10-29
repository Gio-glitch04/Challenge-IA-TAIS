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

## 2026-10-29 — feature/crear-reserva

- PR #2 (persistencia) abierto, apilado sobre #1.
- Supuestos documentados: ADR-008 a ADR-011 (fechas sin zona, sin reservas en el pasado,
  sin límites de duración, 422 para unidad inexistente).
- TDD: `test:` con 21 fallas → `feat:` → 27 passed.

## 2026-10-29 — feature/reglas-superposicion

- PR #3 (crear reserva) abierto.
- El ejemplo de la consigna se usó como fixture de prueba.
- TDD: `test:` con 7 fallas → `feat:` → 40 passed.
