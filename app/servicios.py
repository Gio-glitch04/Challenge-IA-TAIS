"""Reglas de negocio de las reservas. No conoce HTTP; la API traduce los errores."""
import sqlite3
import uuid
from datetime import datetime

from app.esquemas import Intervalo, ReservaEntrada

FORMATO = "%Y-%m-%dT%H:%M:%S"  # formato fijo: permite comparar fechas como texto en SQL


class ErrorDeNegocio(Exception):
    """Regla de negocio incumplida."""


class EntradaInvalida(ErrorDeNegocio):
    pass


class NoEncontrada(ErrorDeNegocio):
    pass


class Conflicto(ErrorDeNegocio):
    pass


def ahora() -> datetime:
    return datetime.now().replace(microsecond=0)


def a_texto(fecha: datetime) -> str:
    return fecha.strftime(FORMATO)


def validar_unidad(con: sqlite3.Connection, unidad_id: str) -> None:
    if con.execute("SELECT 1 FROM unidades WHERE id = ?", (unidad_id,)).fetchone() is None:
        raise EntradaInvalida(f"La unidad '{unidad_id}' no existe en el inventario")


def buscar_conflictos(con: sqlite3.Connection, unidad_id: str, inicio: str, fin: str) -> list:
    """Reservas ACTIVAS de la unidad que se superponen con [inicio, fin).

    Dos intervalos semiabiertos se superponen si cada uno empieza antes de que termine
    el otro. Con desigualdad estricta, un turno que termina a las 11:00 no choca con
    otro que empieza a las 11:00 (turnos consecutivos permitidos).
    """
    filas = con.execute(
        "SELECT * FROM reservas WHERE unidad_id = ? AND estado = 'activa'"
        " AND inicio < ? AND ? < fin ORDER BY inicio",
        (unidad_id, fin, inicio),
    ).fetchall()
    return [dict(f) for f in filas]


def consultar_disponibilidad(con: sqlite3.Connection, unidad_id: str, intervalo: Intervalo) -> dict:
    """Misma regla que la creación: libre si no hay reservas activas superpuestas."""
    if con.execute("SELECT 1 FROM unidades WHERE id = ?", (unidad_id,)).fetchone() is None:
        raise NoEncontrada(f"La unidad '{unidad_id}' no existe en el inventario")
    inicio, fin = a_texto(intervalo.inicio), a_texto(intervalo.fin)
    conflictos = buscar_conflictos(con, unidad_id, inicio, fin)
    return {
        "unidad_id": unidad_id,
        "inicio": inicio,
        "fin": fin,
        "disponible": not conflictos,
        "conflictos": conflictos,
    }


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
        conflictos = buscar_conflictos(
            con, datos.unidad_id, a_texto(datos.inicio), a_texto(datos.fin)
        )
        if conflictos:
            ids = ", ".join(c["id"] for c in conflictos)
            raise Conflicto(
                f"La unidad '{datos.unidad_id}' ya está reservada en ese intervalo"
                f" (reservas: {ids})"
            )
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
