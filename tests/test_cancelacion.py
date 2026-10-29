"""Feature 6: cancelación que conserva el registro y libera el horario."""
import sqlite3

import pytest

RESERVA = {
    "unidad_id": "MIC-01",
    "solicitante": "Ana Prueba",
    "inicio": "2030-05-10T10:00:00",
    "fin": "2030-05-10T11:00:00",
}


@pytest.fixture
def reserva(cliente):
    return cliente.post("/reservas", json=RESERVA).json()


def cancelar(cliente, reserva_id):
    return cliente.post(f"/reservas/{reserva_id}/cancelar")


def test_cancelar_devuelve_la_reserva_con_estado_cancelada(cliente, reserva):
    respuesta = cancelar(cliente, reserva["id"])
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "cancelada"
    assert cuerpo["cancelada_en"] is not None


def test_cancelar_conserva_id_y_todos_los_datos(cliente, reserva):
    cancelar(cliente, reserva["id"])
    guardada = cliente.get(f"/reservas/{reserva['id']}").json()
    for campo in ["id", "unidad_id", "solicitante", "inicio", "fin", "creada_en"]:
        assert guardada[campo] == reserva[campo]
    assert guardada["estado"] == "cancelada"


def test_cancelar_conserva_la_fila_en_la_base(cliente, reserva, ruta_db):
    cancelar(cliente, reserva["id"])
    con = sqlite3.connect(ruta_db)
    filas = con.execute("SELECT id, estado FROM reservas").fetchall()
    con.close()
    assert filas == [(reserva["id"], "cancelada")]


def test_cancelar_libera_el_horario_para_una_nueva_reserva(cliente, reserva):
    assert cliente.post("/reservas", json=RESERVA).status_code == 409
    cancelar(cliente, reserva["id"])
    nueva = cliente.post("/reservas", json={**RESERVA, "solicitante": "Bruno Prueba"})
    assert nueva.status_code == 201
    assert nueva.json()["id"] != reserva["id"]


def test_la_reserva_cancelada_no_bloquea_la_disponibilidad(cliente, reserva):
    params = {"inicio": RESERVA["inicio"], "fin": RESERVA["fin"]}
    assert cliente.get("/unidades/MIC-01/disponibilidad", params=params).json()["disponible"] is False
    cancelar(cliente, reserva["id"])
    cuerpo = cliente.get("/unidades/MIC-01/disponibilidad", params=params).json()
    assert cuerpo["disponible"] is True
    assert cuerpo["conflictos"] == []


def test_cancelar_dos_veces_devuelve_409(cliente, reserva):
    cancelar(cliente, reserva["id"])
    assert cancelar(cliente, reserva["id"]).status_code == 409


def test_cancelar_reserva_inexistente_devuelve_404(cliente):
    assert cancelar(cliente, "no-existe").status_code == 404


def test_listado_incluye_activas_y_canceladas(cliente, reserva):
    otra = cliente.post("/reservas", json={**RESERVA, "unidad_id": "OSC-01"}).json()
    cancelar(cliente, reserva["id"])
    estados = {r["id"]: r["estado"] for r in cliente.get("/reservas").json()}
    assert estados == {reserva["id"]: "cancelada", otra["id"]: "activa"}


def test_listado_filtra_por_unidad_y_estado(cliente, reserva):
    cliente.post("/reservas", json={**RESERVA, "unidad_id": "OSC-01"})
    cancelar(cliente, reserva["id"])
    canceladas = cliente.get("/reservas", params={"estado": "cancelada"}).json()
    assert [r["id"] for r in canceladas] == [reserva["id"]]
    de_osc = cliente.get("/reservas", params={"unidad_id": "OSC-01"}).json()
    assert [r["unidad_id"] for r in de_osc] == ["OSC-01"]


def test_listado_rechaza_estado_desconocido(cliente):
    assert cliente.get("/reservas", params={"estado": "borrada"}).status_code == 422
