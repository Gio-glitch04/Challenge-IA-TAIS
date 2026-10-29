"""Puerto de la API: 8800 por defecto (el 8000 y el 8765 estaban ocupados), configurable con LAB_PORT."""
from app.main import PUERTO_POR_DEFECTO, puerto


def test_puerto_por_defecto_es_8800(monkeypatch):
    monkeypatch.delenv("LAB_PORT", raising=False)
    assert PUERTO_POR_DEFECTO == 8800
    assert puerto() == 8800


def test_lab_port_cambia_el_puerto(monkeypatch):
    monkeypatch.setenv("LAB_PORT", "9123")
    assert puerto() == 9123
