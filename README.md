# API de Registro de Usuarios

API REST desarrollada con FastAPI para gestionar usuarios con operaciones CRUD completas.

## Características

- ? Validación de datos con Pydantic
- ? Operaciones CRUD completas
- ? Validación de correos únicos
- ? Documentación automática con Swagger
- ? Manejo de errores robusto
- ? Validación de edad mínima (18 años)

## Instalación

1. Clonar el repositorio:
```
git clone <tu-repositorio>
cd proyecto-api
```

2. Crear entorno virtual:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. Instalar dependencias:
```
pip install -r requirements.txt
```

## Ejecución

```
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## Documentación

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### POST /usuarios
Crear nuevo usuario
```
{
  "nombre": "Juan Pérez",
  "correo_electronico": "juan@example.com",
  "edad": 25
}
```

### GET /usuarios
Listar todos los usuarios

### GET /usuarios/{id}
Obtener usuario específico

### PUT /usuarios/{id}
Actualizar usuario
```
{
  "nombre": "Juan Carlos Pérez",
  "edad": 26
}
```

### DELETE /usuarios/{id}
Eliminar usuario

## Ejemplos de Uso

```
# Crear usuario
curl -X POST "http://localhost:8000/usuarios" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Ana García","correo_electronico":"ana@example.com","edad":28}'

# Listar usuarios
curl "http://localhost:8000/usuarios"

# Obtener usuario específico
curl "http://localhost:8000/usuarios/1"

# Actualizar usuario
curl -X PUT "http://localhost:8000/usuarios/1" \
  -H "Content-Type: application/json" \
  -d '{"edad":29}'

# Eliminar usuario
curl -X DELETE "http://localhost:8000/usuarios/1"
```

## Validaciones Implementadas

- Nombre: mínimo 2 caracteres, máximo 100
- Email: formato válido
- Edad: entre 18 y 120 años
- Correo electrónico único

## Tecnologías

- FastAPI 0.104.1
- Pydantic 2.5.0
- Uvicorn 0.24.0

## Autor

[Tu Nombre]

## Licencia

MIT
