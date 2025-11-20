from datetime import datetime
from typing import Dict, List

from fastapi import FastAPI, HTTPException, status

from models import Usuario, UsuarioCreate, UsuarioUpdate

app = FastAPI(
    title="API de Registro de Usuarios",
    description="API REST para gestionar usuarios con operaciones CRUD",
    version="1.0.0",
)

# Base de datos en memoria (simulacion)
usuarios_db: Dict[int, Usuario] = {}
contador_id = 1


@app.get("/", tags=["Root"])
def root():
    """Endpoint raiz con informacion de la API."""
    return {
        "mensaje": "Bienvenido a la API de Registro de Usuarios",
        "documentacion": "/docs",
        "version": "1.0.0",
        "endpoints_disponibles": {
            "crear_usuario": "POST /usuarios",
            "listar_usuarios": "GET /usuarios",
            "obtener_usuario": "GET /usuarios/{id}",
            "actualizar_usuario": "PUT /usuarios/{id}",
            "eliminar_usuario": "DELETE /usuarios/{id}",
        },
    }


@app.post(
    "/usuarios",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuarios"],
)
def crear_usuario(usuario: UsuarioCreate):
    """Crea un nuevo usuario en el sistema."""
    global contador_id

    # Verificar si el correo ya existe
    for u in usuarios_db.values():
        if u.correo_electronico == usuario.correo_electronico:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electronico ya esta registrado",
            )

    nuevo_usuario = Usuario(
        id=contador_id,
        nombre=usuario.nombre,
        correo_electronico=usuario.correo_electronico,
        edad=usuario.edad,
        fecha_registro=datetime.now(),
    )

    usuarios_db[contador_id] = nuevo_usuario
    contador_id += 1

    return nuevo_usuario


@app.get("/usuarios", response_model=List[Usuario], tags=["Usuarios"])
def listar_usuarios():
    """Obtiene la lista completa de usuarios registrados."""
    if not usuarios_db:
        return []
    return list(usuarios_db.values())


@app.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
def obtener_usuario(usuario_id: int):
    """Obtiene la informacion de un usuario especifico por su ID."""
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )
    return usuarios_db[usuario_id]


@app.put("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuarios"])
def actualizar_usuario(usuario_id: int, usuario_actualizado: UsuarioUpdate):
    """Actualiza la informacion de un usuario existente."""
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )

    usuario_actual = usuarios_db[usuario_id]

    if usuario_actualizado.correo_electronico:
        for uid, u in usuarios_db.items():
            if uid != usuario_id and u.correo_electronico == usuario_actualizado.correo_electronico:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo electronico ya esta registrado por otro usuario",
                )

    datos_actualizados = usuario_actualizado.dict(exclude_unset=True)

    usuario_nuevo = Usuario(
        id=usuario_actual.id,
        nombre=datos_actualizados.get("nombre", usuario_actual.nombre),
        correo_electronico=datos_actualizados.get(
            "correo_electronico", usuario_actual.correo_electronico
        ),
        edad=datos_actualizados.get("edad", usuario_actual.edad),
        fecha_registro=usuario_actual.fecha_registro,
    )

    usuarios_db[usuario_id] = usuario_nuevo
    return usuario_nuevo


@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_200_OK, tags=["Usuarios"])
def eliminar_usuario(usuario_id: int):
    """Elimina un usuario del sistema."""
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )

    usuario_eliminado = usuarios_db.pop(usuario_id)
    return {"mensaje": "Usuario eliminado exitosamente", "usuario": usuario_eliminado}


@app.get("/health", tags=["Health"])
def health_check():
    """Verifica el estado de la API."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "total_usuarios": len(usuarios_db),
    }
