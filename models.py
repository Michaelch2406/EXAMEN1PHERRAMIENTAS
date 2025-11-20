from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    correo_electronico: EmailStr = Field(..., description="Correo electronico valido")
    edad: int = Field(..., ge=0, le=120, description="Edad del usuario")

    @validator("nombre")
    def validar_nombre(cls, valor: str) -> str:
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacio")
        return valor.strip()

    @validator("edad")
    def validar_edad(cls, valor: int) -> int:
        if valor < 18:
            raise ValueError("El usuario debe ser mayor de 18 anos")
        return valor


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    correo_electronico: Optional[EmailStr] = None
    edad: Optional[int] = Field(None, ge=0, le=120)


class Usuario(UsuarioBase):
    id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True
