"""Feature 3: creación de reservas y validación de entradas."""
import pytest

RESERVA_VALIDA = {
    "unidad_id": "MIC-01",
    "solicitante": "Ana Prueba",
    "inicio": "2030-05-10T10:00:00",
    "fin": "2030-05-10T11:00:00",
}


def con(**cambios):
    return {**RESERVA_VALIDA, **cambios}


# --- Requisito 1: creación válida -------------------------------------------------

def test_creacion_valida_devuelve_201_y_reserva_activa(cliente):
    respuesta = cliente.post("/reservas", json=RESERVA_VALIDA)
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["id"]
    assert cuerpo["estado"] == "activa"
    assert cuerpo["unidad_id"] == "MIC-01"
    assert cuerpo["solicitante"] == "Ana Prueba"
    assert cuerpo["inicio"] == "2030-05-10T10:00:00"
    assert cuerpo["fin"] == "2030-05-10T11:00:00"
    assert cuerpo["cancelada_en"] is None


def test_cada_reserva_tiene_un_id_unico(cliente):
    r1 = cliente.post("/reservas", json=RESERVA_VALIDA).json()
    r2 = cliente.post("/reservas", json=con(unidad_id="OSC-01")).json()
    assert r1["id"] != r2["id"]


def test_la_reserva_creada_se_puede_consultar_por_id(cliente):
    creada = cliente.post("/reservas", json=RESERVA_VALIDA).json()
    respuesta = cliente.get(f"/reservas/{creada['id']}")
    assert respuesta.status_code == 200
    assert respuesta.json() == creada


def test_consultar_reserva_inexistente_devuelve_404(cliente):
    assert cliente.get("/reservas/no-existe").status_code == 404


def test_el_solicitante_se_guarda_sin_espacios_extremos(cliente):
    cuerpo = cliente.post("/reservas", json=con(solicitante="  Ana Prueba  ")).json()
    assert cuerpo["solicitante"] == "Ana Prueba"


# --- Requisito 5: entradas inválidas -----------------------------------------------

@pytest.mark.parametrize("solicitante", ["", "   ", "\t\n"])
def test_rechaza_solicitante_vacio_o_solo_espacios(cliente, solicitante):
    respuesta = cliente.post("/reservas", json=con(solicitante=solicitante))
    assert respuesta.status_code == 422


def test_rechaza_inicio_posterior_al_fin(cliente):
    respuesta = cliente.post(
        "/reservas", json=con(inicio="2030-05-10T12:00:00", fin="2030-05-10T11:00:00")
    )
    assert respuesta.status_code == 422


def test_rechaza_inicio_igual_al_fin(cliente):
    respuesta = cliente.post(
        "/reservas", json=con(inicio="2030-05-10T11:00:00", fin="2030-05-10T11:00:00")
    )
    assert respuesta.status_code == 422


def test_rechaza_unidad_inexistente(cliente):
    respuesta = cliente.post("/reservas", json=con(unidad_id="XYZ-99"))
    assert respuesta.status_code == 422
    assert "XYZ-99" in respuesta.json()["detail"]


@pytest.mark.parametrize(
    "fecha", ["10/05/2030 10:00", "2030-13-01T10:00:00", "mañana", "", 1893456000]
)
def test_rechaza_fechas_que_no_son_iso_8601(cliente, fecha):
    assert cliente.post("/reservas", json=con(inicio=fecha)).status_code == 422


def test_rechaza_fechas_con_zona_horaria(cliente):
    respuesta = cliente.post(
        "/reservas",
        json=con(inicio="2030-05-10T10:00:00+00:00", fin="2030-05-10T11:00:00+00:00"),
    )
    assert respuesta.status_code == 422


def test_rechaza_reservas_que_empiezan_en_el_pasado(cliente):
    respuesta = cliente.post(
        "/reservas", json=con(inicio="2020-01-01T10:00:00", fin="2020-01-01T11:00:00")
    )
    assert respuesta.status_code == 422


@pytest.mark.parametrize("campo", ["unidad_id", "solicitante", "inicio", "fin"])
def test_rechaza_campos_faltantes(cliente, campo):
    datos = dict(RESERVA_VALIDA)
    del datos[campo]
    assert cliente.post("/reservas", json=datos).status_code == 422
