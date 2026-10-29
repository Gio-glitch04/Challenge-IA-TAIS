# Contexto estable del proyecto

- **Objetivo:** API local para reservar equipos de laboratorio sin superposiciones y sin
  perder el historial de cancelaciones. Especificación completa: `Harness/specs.md`.
- **Stack:** Python 3.10+, FastAPI + Uvicorn, SQLite (`sqlite3` de la biblioteca estándar),
  Pydantic v2, pytest + httpx.
- **Inventario (solo lectura):** MIC-01 y MIC-02 (Microscopio digital), OSC-01
  (Osciloscopio), MUL-01 (Multímetro), FUE-01 (Fuente de alimentación).
- **Reglas críticas:**
  - la unidad debe existir;
  - solicitante no vacío ni solo espacios;
  - inicio estrictamente anterior al fin;
  - se rechaza la superposición con reservas *activas* de la misma unidad;
  - se permiten turnos consecutivos (fin == inicio) y la misma franja en unidades distintas;
  - una reserva cancelada no bloquea y se conserva en la base.
- **Persistencia:** archivo SQLite; reiniciar Uvicorn no borra datos. El borrado solo se
  hace con un script explícito.
- **Fuera de alcance:** autenticación, roles, notificaciones, interfaz gráfica,
  concurrencia distribuida, integraciones externas.
- **Convenciones:** código y documentación en español; ramas `feature/*`; commits
  semánticos; sin el nombre del asistente en ramas, commits ni PRs.
