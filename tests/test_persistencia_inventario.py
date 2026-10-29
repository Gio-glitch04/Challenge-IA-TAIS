"""Feature 2: base SQLite con inventario precargado y reinicio explícito."""
import sqlite3
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import crear_app

INVENTARIO_ESPERADO = [
    {"id": "FUE-01", "equipo": "Fuente de alimentación"},
    {"id": "MIC-01", "equipo": "Microscopio digital"},
    {"id": "MIC-02", "equipo": "Microscopio digital"},
    {"id": "MUL-01", "equipo": "Multímetro"},
    {"id": "OSC-01", "equipo": "Osciloscopio"},
]
RAIZ = Path(__file__).resolve().parent.parent


def test_lista_el_inventario_precargado(cliente):
    respuesta = cliente.get("/unidades")
    assert respuesta.status_code == 200
    assert respuesta.json() == INVENTARIO_ESPERADO


def test_crea_el_archivo_sqlite(cliente, ruta_db):
    assert ruta_db.exists()


def test_reiniciar_la_app_no_duplica_ni_borra_datos(ruta_db):
    with TestClient(crear_app(ruta_db)):
        pass
    # Simula datos previos escritos por la app en otra ejecución.
    con = sqlite3.connect(ruta_db)
    con.execute(
        "INSERT INTO reservas (id, unidad_id, solicitante, inicio, fin, estado, creada_en)"
        " VALUES ('r1', 'MIC-01', 'Ana Prueba', '2030-01-01T10:00:00',"
        " '2030-01-01T11:00:00', 'activa', '2026-10-29T12:00:00')"
    )
    con.commit()
    con.close()

    with TestClient(crear_app(ruta_db)) as cliente:
        assert cliente.get("/unidades").json() == INVENTARIO_ESPERADO

    con = sqlite3.connect(ruta_db)
    assert con.execute("SELECT COUNT(*) FROM reservas").fetchone()[0] == 1
    con.close()


def test_script_de_reinicio_exige_confirmacion(ruta_db):
    with TestClient(crear_app(ruta_db)):
        pass
    entorno = {"LAB_DB_PATH": str(ruta_db), "PATH": ""}
    sin_flag = subprocess.run(
        [sys.executable, "-m", "scripts.reset_db"], cwd=RAIZ, env=entorno,
        capture_output=True, text=True,
    )
    assert sin_flag.returncode == 1
    assert ruta_db.exists()


def test_script_de_reinicio_borra_reservas_y_recarga_inventario(ruta_db):
    with TestClient(crear_app(ruta_db)):
        pass
    con = sqlite3.connect(ruta_db)
    con.execute(
        "INSERT INTO reservas (id, unidad_id, solicitante, inicio, fin, estado, creada_en)"
        " VALUES ('r1', 'MIC-01', 'Ana Prueba', '2030-01-01T10:00:00',"
        " '2030-01-01T11:00:00', 'activa', '2026-10-29T12:00:00')"
    )
    con.commit()
    con.close()

    resultado = subprocess.run(
        [sys.executable, "-m", "scripts.reset_db", "--si"], cwd=RAIZ,
        env={"LAB_DB_PATH": str(ruta_db), "PATH": ""}, capture_output=True, text=True,
    )
    assert resultado.returncode == 0, resultado.stderr

    con = sqlite3.connect(ruta_db)
    assert con.execute("SELECT COUNT(*) FROM reservas").fetchone()[0] == 0
    assert con.execute("SELECT COUNT(*) FROM unidades").fetchone()[0] == 5
    con.close()
