"""API local de reservas de equipos de laboratorio."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException

from app import servicios
from app.database import conectar, inicializar_db, ruta_db
from app.esquemas import Reserva, ReservaEntrada

CODIGOS_HTTP = {
    servicios.EntradaInvalida: 422,
    servicios.NoEncontrada: 404,
    servicios.Conflicto: 409,
}


def crear_app(ruta: Optional[Path] = None) -> FastAPI:
    """Crea la aplicación. `ruta` permite a las pruebas usar una base temporal."""
    ruta = Path(ruta) if ruta else ruta_db()

    @asynccontextmanager
    async def ciclo_de_vida(app: FastAPI):
        inicializar_db(ruta)  # idempotente: nunca borra reservas
        yield

    app = FastAPI(title="Reservas de laboratorio", lifespan=ciclo_de_vida)

    def ejecutar(operacion, *args):
        """Abre una conexión, corre la operación y traduce errores de negocio a HTTP."""
        con = conectar(ruta)
        try:
            return operacion(con, *args)
        except servicios.ErrorDeNegocio as error:
            raise HTTPException(CODIGOS_HTTP[type(error)], str(error))
        finally:
            con.close()

    @app.get("/unidades")
    def listar_unidades():
        filas = ejecutar(
            lambda con: con.execute("SELECT id, equipo FROM unidades ORDER BY id").fetchall()
        )
        return [dict(f) for f in filas]

    @app.post("/reservas", response_model=Reserva, status_code=201)
    def crear_reserva(datos: ReservaEntrada):
        return ejecutar(servicios.crear_reserva, datos)

    @app.get("/reservas/{reserva_id}", response_model=Reserva)
    def obtener_reserva(reserva_id: str):
        return ejecutar(servicios.obtener_reserva, reserva_id)

    return app


app = crear_app()
