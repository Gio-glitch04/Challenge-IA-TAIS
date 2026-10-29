"""API local de reservas de equipos de laboratorio."""
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Literal, Optional

from fastapi import FastAPI, HTTPException, Query

from app import servicios
from app.database import conectar, inicializar_db, ruta_db
from app.esquemas import Disponibilidad, Intervalo, Reserva, ReservaEntrada

CODIGOS_HTTP = {
    servicios.EntradaInvalida: 422,
    servicios.NoEncontrada: 404,
    servicios.Conflicto: 409,
}

# El 8000 (default de Uvicorn) y el 8765 estaban ocupados en la máquina del autor.
PUERTO_POR_DEFECTO = 8800


def puerto() -> int:
    """Puerto de la API: variable LAB_PORT o 8800."""
    return int(os.environ.get("LAB_PORT", PUERTO_POR_DEFECTO))


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

    @app.get("/unidades/{unidad_id}/disponibilidad", response_model=Disponibilidad)
    def consultar_disponibilidad(unidad_id: str, intervalo: Annotated[Intervalo, Query()]):
        return ejecutar(servicios.consultar_disponibilidad, unidad_id, intervalo)

    @app.post("/reservas", response_model=Reserva, status_code=201)
    def crear_reserva(datos: ReservaEntrada):
        return ejecutar(servicios.crear_reserva, datos)

    @app.get("/reservas", response_model=list[Reserva])
    def listar_reservas(
        unidad_id: Optional[str] = None,
        estado: Optional[Literal["activa", "cancelada"]] = None,
    ):
        return ejecutar(servicios.listar_reservas, unidad_id, estado)

    @app.post("/reservas/{reserva_id}/cancelar", response_model=Reserva)
    def cancelar_reserva(reserva_id: str):
        return ejecutar(servicios.cancelar_reserva, reserva_id)

    @app.get("/reservas/{reserva_id}", response_model=Reserva)
    def obtener_reserva(reserva_id: str):
        return ejecutar(servicios.obtener_reserva, reserva_id)

    return app


app = crear_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=puerto())
