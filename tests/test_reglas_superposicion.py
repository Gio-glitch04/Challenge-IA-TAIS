"""Feature 4: superposición, turnos consecutivos y unidades simultáneas.

Escenario de la consigna: MIC-01 reservado de 10:00 a 11:00.
"""
import pytest

DIA = "2030-05-10"


def reservar(cliente, unidad, inicio, fin, solicitante="Ana Prueba"):
    return cliente.post(
        "/reservas",
        json={
            "unidad_id": unidad,
            "solicitante": solicitante,
            "inicio": f"{DIA}T{inicio}:00",
            "fin": f"{DIA}T{fin}:00",
        },
    )


@pytest.fixture
def mic01_de_10_a_11(cliente):
    respuesta = reservar(cliente, "MIC-01", "10:00", "11:00")
    assert respuesta.status_code == 201
    return respuesta.json()


# --- Requisito 2: rechazo por superposición ----------------------------------------

def test_rechaza_superposicion_del_ejemplo_de_la_consigna(cliente, mic01_de_10_a_11):
    respuesta = reservar(cliente, "MIC-01", "10:30", "11:30", "Bruno Prueba")
    assert respuesta.status_code == 409
    assert mic01_de_10_a_11["id"] in respuesta.json()["detail"]


@pytest.mark.parametrize(
    "inicio, fin",
    [
        ("09:30", "10:30"),  # se pisa por el inicio
        ("10:15", "10:45"),  # contenida
        ("09:00", "12:00"),  # la contiene
        ("10:00", "11:00"),  # idéntica
        ("10:00", "10:01"),  # mismo inicio
        ("10:59", "11:00"),  # mismo fin
    ],
)
def test_rechaza_toda_forma_de_superposicion(cliente, mic01_de_10_a_11, inicio, fin):
    assert reservar(cliente, "MIC-01", inicio, fin).status_code == 409


def test_la_reserva_rechazada_no_se_guarda(cliente, mic01_de_10_a_11):
    reservar(cliente, "MIC-01", "10:30", "11:30")
    assert reservar(cliente, "MIC-01", "11:00", "12:00").status_code == 201


# --- Requisito 3: límites consecutivos ---------------------------------------------

def test_acepta_turno_que_empieza_cuando_termina_otro(cliente, mic01_de_10_a_11):
    assert reservar(cliente, "MIC-01", "11:00", "12:00").status_code == 201


def test_acepta_turno_que_termina_cuando_empieza_otro(cliente, mic01_de_10_a_11):
    assert reservar(cliente, "MIC-01", "09:00", "10:00").status_code == 201


def test_acepta_hueco_exacto_entre_dos_reservas(cliente):
    assert reservar(cliente, "MIC-01", "09:00", "10:00").status_code == 201
    assert reservar(cliente, "MIC-01", "11:00", "12:00").status_code == 201
    assert reservar(cliente, "MIC-01", "10:00", "11:00").status_code == 201


# --- Requisito 4: unidades distintas simultáneas -----------------------------------

def test_acepta_mic02_en_el_mismo_horario_que_mic01(cliente, mic01_de_10_a_11):
    assert reservar(cliente, "MIC-02", "10:00", "11:00").status_code == 201


def test_acepta_todas_las_unidades_en_el_mismo_horario(cliente):
    for unidad in ["MIC-01", "MIC-02", "OSC-01", "MUL-01", "FUE-01"]:
        assert reservar(cliente, unidad, "10:00", "11:00").status_code == 201
