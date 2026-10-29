"""Acceso a SQLite: creación del esquema y carga idempotente del inventario."""
import json
import os
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RUTA_DB_POR_DEFECTO = RAIZ / "data" / "laboratorio.db"
RUTA_INVENTARIO = Path(__file__).resolve().parent / "inventario.json"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS unidades (
    id     TEXT PRIMARY KEY,
    equipo TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reservas (
    id           TEXT PRIMARY KEY,
    unidad_id    TEXT NOT NULL REFERENCES unidades(id),
    solicitante  TEXT NOT NULL,
    inicio       TEXT NOT NULL,
    fin          TEXT NOT NULL,
    estado       TEXT NOT NULL CHECK (estado IN ('activa', 'cancelada')),
    creada_en    TEXT NOT NULL,
    cancelada_en TEXT,
    CHECK (inicio < fin)
);
CREATE INDEX IF NOT EXISTS idx_reservas_unidad_estado
    ON reservas (unidad_id, estado, inicio, fin);
"""


def ruta_db() -> Path:
    """Ruta del archivo SQLite. Se puede cambiar con la variable LAB_DB_PATH."""
    return Path(os.environ.get("LAB_DB_PATH", RUTA_DB_POR_DEFECTO))


def conectar(ruta: Path) -> sqlite3.Connection:
    conexion = sqlite3.connect(ruta, isolation_level=None)  # transacciones explícitas
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_db(ruta: Path) -> None:
    """Crea tablas si faltan y carga el inventario. Nunca borra reservas."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    inventario = json.loads(RUTA_INVENTARIO.read_text(encoding="utf-8"))
    conexion = conectar(ruta)
    try:
        conexion.executescript(ESQUEMA)
        conexion.executemany(
            "INSERT OR IGNORE INTO unidades (id, equipo) VALUES (:id, :equipo)",
            inventario,
        )
    finally:
        conexion.close()
