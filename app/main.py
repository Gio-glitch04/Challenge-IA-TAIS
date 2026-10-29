"""API local de reservas de equipos de laboratorio."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI

from app.database import conectar, inicializar_db, ruta_db


def crear_app(ruta: Optional[Path] = None) -> FastAPI:
    """Crea la aplicación. `ruta` permite a las pruebas usar una base temporal."""
    ruta = Path(ruta) if ruta else ruta_db()

    @asynccontextmanager
    async def ciclo_de_vida(app: FastAPI):
        inicializar_db(ruta)  # idempotente: nunca borra reservas
        yield

    app = FastAPI(title="Reservas de laboratorio", lifespan=ciclo_de_vida)

    @app.get("/unidades")
    def listar_unidades():
        con = conectar(ruta)
        try:
            filas = con.execute("SELECT id, equipo FROM unidades ORDER BY id").fetchall()
        finally:
            con.close()
        return [dict(f) for f in filas]

    return app


app = crear_app()
