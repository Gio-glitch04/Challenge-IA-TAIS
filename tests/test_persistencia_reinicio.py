"""Persistencia de reservas activas y canceladas al detener y reiniciar la app.

Cada bloque `with TestClient(...)` arranca y apaga la aplicación completa (lifespan),
igual que detener y volver a levantar Uvicorn sobre el mismo archivo SQLite.
"""
from fastapi.testclient import TestClient

from app.main import crear_app

BASE = {"solicitante": "Ana Prueba", "inicio": "2030-05-10T10:00:00", "fin": "2030-05-10T11:00:00"}


def test_activas_y_canceladas_sobreviven_al_reinicio(ruta_db):
    with TestClient(crear_app(ruta_db)) as primera_ejecucion:
        activa = primera_ejecucion.post("/reservas", json={**BASE, "unidad_id": "MIC-01"}).json()
        cancelada = primera_ejecucion.post("/reservas", json={**BASE, "unidad_id": "MIC-02"}).json()
        primera_ejecucion.post(f"/reservas/{cancelada['id']}/cancelar")

    with TestClient(crear_app(ruta_db)) as segunda_ejecucion:
        assert segunda_ejecucion.get(f"/reservas/{activa['id']}").json()["estado"] == "activa"
        recuperada = segunda_ejecucion.get(f"/reservas/{cancelada['id']}").json()
        assert recuperada["estado"] == "cancelada"
        assert recuperada["solicitante"] == "Ana Prueba"

        # La activa sigue bloqueando y la cancelada sigue liberada.
        assert segunda_ejecucion.post("/reservas", json={**BASE, "unidad_id": "MIC-01"}).status_code == 409
        assert segunda_ejecucion.post("/reservas", json={**BASE, "unidad_id": "MIC-02"}).status_code == 201
