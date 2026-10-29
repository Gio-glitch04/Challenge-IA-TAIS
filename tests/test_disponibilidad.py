"""Feature 5: consulta de disponibilidad por unidad e intervalo.

Debe aplicar exactamente las mismas reglas que la creación de reservas.
"""
import pytest

DIA = "2030-05-10"


def fecha(hora):
    return f"{DIA}T{hora}:00"


def reservar(cliente, unidad, inicio, fin):
    return cliente.post(
        "/reservas",
        json={"unidad_id": unidad, "solicitante": "Ana Prueba",
              "inicio": fecha(inicio), "fin": fecha(fin)},
    )


def consultar(cliente, unidad, inicio, fin):
    return cliente.get(
        f"/unidades/{unidad}/disponibilidad",
        params={"inicio": fecha(inicio), "fin": fecha(fin)},
    )


@pytest.fixture
def mic01_de_10_a_11(cliente):
    return reservar(cliente, "MIC-01", "10:00", "11:00").json()


def test_unidad_sin_reservas_esta_disponible(cliente):
    respuesta = consultar(cliente, "MIC-01", "10:00", "11:00")
    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "unidad_id": "MIC-01",
        "inicio": fecha("10:00"),
        "fin": fecha("11:00"),
        "disponible": True,
        "conflictos": [],
    }


def test_intervalo_superpuesto_no_esta_disponible_y_muestra_el_conflicto(
    cliente, mic01_de_10_a_11
):
    cuerpo = consultar(cliente, "MIC-01", "10:30", "11:30").json()
    assert cuerpo["disponible"] is False
    assert [c["id"] for c in cuerpo["conflictos"]] == [mic01_de_10_a_11["id"]]


def test_turno_consecutivo_esta_disponible(cliente, mic01_de_10_a_11):
    assert consultar(cliente, "MIC-01", "11:00", "12:00").json()["disponible"] is True


def test_otra_unidad_en_el_mismo_horario_esta_disponible(cliente, mic01_de_10_a_11):
    assert consultar(cliente, "MIC-02", "10:00", "11:00").json()["disponible"] is True


def test_consultar_no_crea_reservas(cliente):
    consultar(cliente, "MIC-01", "10:00", "11:00")
    assert reservar(cliente, "MIC-01", "10:00", "11:00").status_code == 201


@pytest.mark.parametrize(
    "inicio, fin",
    [("09:00", "10:00"), ("09:30", "10:30"), ("10:00", "11:00"), ("10:15", "10:45"),
     ("10:59", "11:30"), ("11:00", "12:00"), ("08:00", "13:00")],
)
def test_disponibilidad_coincide_con_lo_que_acepta_la_creacion(
    cliente, mic01_de_10_a_11, inicio, fin
):
    disponible = consultar(cliente, "MIC-01", inicio, fin).json()["disponible"]
    creada = reservar(cliente, "MIC-01", inicio, fin).status_code == 201
    assert disponible == creada


def test_unidad_inexistente_devuelve_404(cliente):
    assert consultar(cliente, "XYZ-99", "10:00", "11:00").status_code == 404


def test_rechaza_inicio_posterior_al_fin(cliente):
    assert consultar(cliente, "MIC-01", "12:00", "11:00").status_code == 422


def test_rechaza_inicio_igual_al_fin(cliente):
    assert consultar(cliente, "MIC-01", "11:00", "11:00").status_code == 422


def test_rechaza_fecha_invalida(cliente):
    respuesta = cliente.get(
        "/unidades/MIC-01/disponibilidad", params={"inicio": "ayer", "fin": fecha("11:00")}
    )
    assert respuesta.status_code == 422


def test_rechaza_parametros_faltantes(cliente):
    assert cliente.get("/unidades/MIC-01/disponibilidad").status_code == 422


def test_permite_consultar_intervalos_pasados(cliente):
    respuesta = cliente.get(
        "/unidades/MIC-01/disponibilidad",
        params={"inicio": "2020-01-01T10:00:00", "fin": "2020-01-01T11:00:00"},
    )
    assert respuesta.status_code == 200
