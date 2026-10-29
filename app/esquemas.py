"""Modelos Pydantic de entrada y salida de la API."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


def parsear_fecha_iso(valor) -> datetime:
    """Acepta solo texto ISO 8601 sin zona horaria (hora local del laboratorio)."""
    if not isinstance(valor, str):
        raise ValueError("La fecha debe ser texto en formato ISO 8601 (AAAA-MM-DDTHH:MM[:SS])")
    try:
        fecha = datetime.fromisoformat(valor)
    except ValueError:
        raise ValueError("Fecha inválida: usar ISO 8601, por ejemplo 2030-05-10T10:00:00")
    if fecha.tzinfo is not None:
        raise ValueError("No se admite zona horaria: las fechas son hora local del laboratorio")
    if fecha.microsecond:
        raise ValueError("La precisión máxima es de segundos")
    return fecha


class Intervalo(BaseModel):
    inicio: datetime
    fin: datetime

    @field_validator("inicio", "fin", mode="before")
    @classmethod
    def _fecha_iso(cls, valor):
        return parsear_fecha_iso(valor)

    @model_validator(mode="after")
    def _inicio_antes_que_fin(self):
        if self.inicio >= self.fin:
            raise ValueError("El inicio debe ser estrictamente anterior al fin")
        return self


class ReservaEntrada(Intervalo):
    unidad_id: str
    solicitante: str = Field(max_length=100)

    @field_validator("solicitante")
    @classmethod
    def _solicitante_no_vacio(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("El solicitante no puede estar vacío ni ser solo espacios")
        return valor


class Reserva(BaseModel):
    id: str
    unidad_id: str
    solicitante: str
    inicio: str
    fin: str
    estado: str
    creada_en: str
    cancelada_en: Optional[str] = None
