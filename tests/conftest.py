import pytest
from fastapi.testclient import TestClient

from app.main import crear_app


@pytest.fixture
def ruta_db(tmp_path):
    """Cada prueba usa su propio archivo SQLite temporal."""
    return tmp_path / "prueba.db"


@pytest.fixture
def cliente(ruta_db):
    with TestClient(crear_app(ruta_db)) as c:
        yield c
