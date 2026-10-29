"""Feature 6: interfaz web mínima servida por la misma API, sin lógica de negocio propia."""


def test_la_raiz_sirve_la_pagina_html(cliente):
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert respuesta.headers["content-type"].startswith("text/html")
    assert "Reservas de laboratorio" in respuesta.text


def test_la_pagina_tiene_las_tres_operaciones(cliente):
    html = cliente.get("/").text
    for id_formulario in ('id="form-disponibilidad"', 'id="form-reserva"', 'id="tabla-reservas"'):
        assert id_formulario in html


def test_la_pagina_solo_usa_los_endpoints_de_la_api(cliente):
    """La interfaz no tiene reglas propias: todo pasa por los mismos endpoints."""
    html = cliente.get("/").text
    for ruta in ("/unidades", "/disponibilidad", "/reservas", "/cancelar"):
        assert ruta in html


def test_la_pagina_no_aparece_en_el_esquema_de_la_api(cliente):
    assert "/" not in cliente.get("/openapi.json").json()["paths"]
