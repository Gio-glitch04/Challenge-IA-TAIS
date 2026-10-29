# Bitácora de sesiones

Registro cronológico, solo se agregan entradas al final.

## 2026-10-29 — chore/preparar-entorno

- Se leyeron la consigna del challenge y `Harness/specs.md`.
- Acuerdo con el responsable (Giovanni): la preparación del entorno va en un PR propio que no
  cuenta como feature; las features de la aplicación van de a una, cada una con su rama, su
  PR contra `main` y su documentación en `docs/`.
- Se creó `AGENTS.md` con identidad, memoria local, estrategia de ramas y límites de
  autonomía, y el sistema de memoria `.memoria/` (contexto, estado, bitácora).

## 2026-10-29 — feature/persistencia-inventario (feature 1)

- PR de preparación del entorno (#9) mergeado por Giovanni (`9914fa1`).
- TDD: commit `test:` con las pruebas en rojo, después commit `feat:` con la implementación.
- `python -m pytest -v` → 5 passed.
- Prueba manual: `uvicorn app.main:app` + `curl /unidades` devolvió las 5 unidades.
