"""Reinicia la base de datos: BORRA TODAS LAS RESERVAS y recarga el inventario.

Uso:  python -m scripts.reset_db --si
Sin el flag --si no hace nada. La ejecución normal de la API nunca borra datos.
"""
import sys

from app.database import inicializar_db, ruta_db


def main() -> int:
    ruta = ruta_db()
    if "--si" not in sys.argv:
        print(f"Esto borrará {ruta} con todas sus reservas. Repetí con --si para confirmar.")
        return 1
    if ruta.exists():
        ruta.unlink()
    inicializar_db(ruta)
    print(f"Base reiniciada en {ruta} (inventario recargado, 0 reservas).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
