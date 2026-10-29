"""Reglas de negocio de las reservas. No conoce HTTP; la API traduce los errores."""
import sqlite3
import uuid
from datetime import datetime

from app.esquemas import ReservaEntrada

FORMATO = "%Y-%m-%dT%H:%M:%S"  # formato fijo: permite comparar fechas como texto en SQL


class ErrorDeNegocio(Exception):
    """Regla de negocio incumplida."""


class EntradaInvalida(ErrorDeNegocio):
    pass


class NoEncontrada(ErrorDeNegocio):
    pass


def ahora() -> datetime:
    return datetime.now().replace(microsecond=0)


def a_texto(fecha: datetime) -> str:
    return fecha.strftime(FORMATO)


def validar_unidad(con: sqlite3.Connection, unidad_id: str) -> None:
    if con.execute("SELECT 1 FROM unidades WHERE id = ?", (unidad_id,)).fetchone() is None:
        raise EntradaInvalida(f"La unidad '{unidad_id}' no existe en el inventario")


def obtener_reserva(con: sqlite3.Connection, reserva_id: str) -> dict:
    fila = con.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()
    if fila is None:
        raise NoEncontrada(f"No existe la reserva '{reserva_id}'")
    return dict(fila)


def crear_reserva(con: sqlite3.Connection, datos: ReservaEntrada) -> dict:
    if datos.inicio < ahora():
        raise EntradaInvalida("No se puede reservar un intervalo que empieza en el pasado")
    con.execute("BEGIN IMMEDIATE")  # validación + alta en una sola transacción
    try:
        validar_unidad(con, datos.unidad_id)
        reserva = {
            "id": str(uuid.uuid4()),
            "unidad_id": datos.unidad_id,
            "solicitante": datos.solicitante,
            "inicio": a_texto(datos.inicio),
            "fin": a_texto(datos.fin),
            "estado": "activa",
            "creada_en": a_texto(ahora()),
            "cancelada_en": None,
        }
        con.execute(
            "INSERT INTO reservas (id, unidad_id, solicitante, inicio, fin, estado,"
            " creada_en, cancelada_en) VALUES (:id, :unidad_id, :solicitante, :inicio,"
            " :fin, :estado, :creada_en, :cancelada_en)",
            reserva,
        )
        con.execute("COMMIT")
    except BaseException:
        con.execute("ROLLBACK")
        raise
    return reserva
