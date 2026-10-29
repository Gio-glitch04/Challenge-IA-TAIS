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

## 2026-10-29 — feature/crear-reserva (feature 2)

- PR #10 (feature 1) mergeado por Giovanni (`41a4c02`).
- Supuestos documentados: ADR-005 a ADR-008 (fechas sin zona, sin reservas en el pasado,
  sin límites de duración, 422 para unidad inexistente).
- TDD: `test:` con 21 fallas → `feat:` → 27 passed.

## 2026-10-29 — feature/reglas-superposicion (feature 3)

- PR #11 (feature 2) mergeado por Giovanni (`35afb1b`), sin cambios en los supuestos.
- El ejemplo de la consigna se usó como fixture de prueba.
- TDD: `test:` con 7 fallas → `feat:` → 40 passed.

## 2026-10-29 — feature/disponibilidad (feature 4)

- PR #12 (feature 3) mergeado por Giovanni (`5f7371b`).
- TDD: `test:` con 16 fallas → `feat:` → 58 passed.

## 2026-10-29 — feature/cancelacion (feature 5)

- PR #13 (feature 4) mergeado por Giovanni (`984b841`).
- TDD: `test:` con 10 fallas → `feat:` → 69 passed.
- Procedimiento manual: 2 ejecuciones de Uvicorn sobre `data/manual-reinicio.db`; la
  reserva activa y la cancelada se recuperaron con sus datos (archivo borrado al final).

## 2026-10-29 — docs/readme

- PR #14 (feature 5) mergeado por Giovanni (`b39b09a`).
- README final con las 4 secciones de la consigna. Episodios elegidos: superposición (03),
  cancelación y reinicio (05) y la corrección de la organización de PRs (#2 a #8 cerrados,
  rehechos como #9 a #14).
- Ejemplo de entrada y salida ejecutado con TestClient; `python -m pytest -q` → 69 passed.

## 2026-10-29 — docs/readme-windows

- PR #15 (README) mergeado por Giovanni (`c2545e8`).
- Pedido del autor: instalación y guía de uso al inicio del README, con comandos de Windows.
- Se movió la guía arriba de la sección 1, con PowerShell (`Invoke-RestMethod`) y las
  variantes de `cmd`. Los endpoints de la guía se ejecutaron con `curl` contra Uvicorn
  (Linux); PowerShell no está disponible en el contenedor.
- `python -m pytest -q` → 69 passed.

## 2026-10-29 — fix/puerto-api

- PR #16 (guía de Windows) mergeado por Giovanni (`142c43c`).
- Pedido del autor: cambiar el puerto porque el 8000 está ocupado en su máquina.
- TDD: `test:` con error de colección (no existía `puerto`) → `feat:` → 71 passed.
- Prueba manual: `python -m app.main` respondió en 8765 y con `LAB_PORT=9123` en 9123.

## 2026-10-29 — fix/puerto-8800

- PR #17 (puerto 8765) mergeado por Giovanni.
- El 8765 también estaba ocupado en su máquina; eligió el 8800.
- TDD: `test:` con 1 falla → `fix:` → 71 passed. `python -m app.main` respondió en 8800.
