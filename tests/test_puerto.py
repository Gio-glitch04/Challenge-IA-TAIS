"""Puerto de la API: 8765 por defecto (el 8000 suele estar ocupado), configurable con LAB_PORT."""
from app.main import PUERTO_POR_DEFECTO, puerto


def test_puerto_por_defecto_es_8765(monkeypatch):
    monkeypatch.delenv("LAB_PORT", raising=False)
    assert PUERTO_POR_DEFECTO == 8765
    assert puerto() == 8765


def test_lab_port_cambia_el_puerto(monkeypatch):
    monkeypatch.setenv("LAB_PORT", "9123")
    assert puerto() == 9123
