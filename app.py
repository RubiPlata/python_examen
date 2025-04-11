from flask import Flask, jsonify
from flask_cors import CORS
from config import db, migrate
from dotenv import load_dotenv
import os
from routes.user import user_bp
from flask_swagger_ui import get_swaggerui_blueprint

load_dotenv()

app = Flask(__name__)

# Configuración CORS más completa
CORS(app, resources={
    r"/api/*": {"origins": "*"},
    r"/users/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    },
    r"/swagger.json": {"origins": "*"}
})

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de extensiones
db.init_app(app)
migrate.init_app(app, db)

# Registrar blueprint de usuarios con prefijo '/users'
app.register_blueprint(user_bp, url_prefix='/users')

# Configuración Swagger UI
SWAGGER_URL = '/api/docs'  # URL para acceder a la UI de Swagger
API_URL = '/swagger.json'  # URL para el archivo JSON de especificación

# Crear blueprint de Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Usuarios",
        'validatorUrl': None,
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete']
    }
)

# Registrar el blueprint de Swagger UI
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
# Ruta para servir el archivo swagger.json
@app.route(API_URL)
def swagger():
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "API de Usuarios",
            "description": "API para gestión de usuarios (registro, autenticación, CRUD)",
            "version": "1.0"
        },
        "basePath": "/users",  # Añadido el basePath para evitar duplicación
        "tags": [
            {
                "name": "Usuarios",
                "description": "Operaciones relacionadas con usuarios"
            }
        ],
        "paths": {
            "/users": {  # Cambiado de "users/users" a "/users"
                "get": {
                    "tags": ["Usuarios"],
                    "summary": "Obtener todos los usuarios",
                    "description": "Retorna una lista con todos los usuarios registrados",
                    "responses": {
                        "200": {
                            "description": "Lista de usuarios obtenida exitosamente",
                            "schema": {
                                "type": "array",
                                "items": {"$ref": "#/definitions/User"}
                            }
                        },
                        "500": {"description": "Error interno del servidor"}
                    }
                },
                "post": {
                    "tags": ["Usuarios"],
                    "summary": "Registrar un nuevo usuario",
                    "description": "Crea un nuevo usuario en el sistema con contraseña hasheada",
                    "parameters": [
                        {
                            "in": "body",
                            "name": "body",
                            "description": "Datos del usuario a registrar",
                            "required": True,
                            "schema": {"$ref": "#/definitions/UserRegister"}
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Usuario registrado exitosamente",
                            "schema": {"$ref": "#/definitions/User"}
                        },
                        "400": {"description": "El email ya está registrado o datos inválidos"},
                        "500": {"description": "Error interno del servidor"}
                    }
                }
            },
            "/{user_id}": {  # Cambiado de "/users/{user_id}" a "/{user_id}"
                "get": {
                    "tags": ["Usuarios"],
                    "summary": "Obtener usuario por ID",
                    "description": "Retorna la información de un usuario específico",
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "description": "ID del usuario",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Usuario encontrado",
                            "schema": {"$ref": "#/definitions/User"}
                        },
                        "404": {"description": "Usuario no encontrado"},
                        "500": {"description": "Error interno del servidor"}
                    }
                },
                "put": {
                    "tags": ["Usuarios"],
                    "summary": "Actualizar usuario",
                    "description": "Actualiza la información de un usuario existente",
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "description": "ID del usuario",
                            "required": True,
                            "type": "integer"
                        },
                        {
                            "in": "body",
                            "name": "body",
                            "description": "Datos del usuario a actualizar",
                            "required": True,
                            "schema": {"$ref": "#/definitions/UserUpdate"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Usuario actualizado exitosamente",
                            "schema": {"$ref": "#/definitions/User"}
                        },
                        "404": {"description": "Usuario no encontrado"},
                        "500": {"description": "Error interno del servidor"}
                    }
                },
                "delete": {
                    "tags": ["Usuarios"],
                    "summary": "Eliminar usuario",
                    "description": "Elimina un usuario del sistema",
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "description": "ID del usuario",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Usuario eliminado exitosamente",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "User deleted successfully"
                                    }
                                }
                            }
                        },
                        "404": {"description": "Usuario no encontrado"},
                        "500": {"description": "Error interno del servidor"}
                    }
                }
            },
            "/login": {  # Cambiado de "users/login" a "/login"
                "post": {
                    "tags": ["Usuarios"],
                    "summary": "Autenticar usuario",
                    "description": "Verifica las credenciales y autentica un usuario",
                    "parameters": [
                        {
                            "in": "body",
                            "name": "body",
                            "description": "Credenciales de autenticación",
                            "required": True,
                            "schema": {"$ref": "#/definitions/UserLogin"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Autenticación exitosa",
                            "schema": {"$ref": "#/definitions/User"}
                        },
                        "401": {"description": "Credenciales inválidas"},
                        "404": {"description": "Usuario no encontrado"},
                        "500": {"description": "Error interno del servidor"}
                    }
                }
            }
        },
        "definitions": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "ID único del usuario"},
                    "name": {"type": "string", "description": "Nombre completo del usuario"},
                    "email": {"type": "string", "format": "email", "description": "Email del usuario"}
                },
                "required": ["id", "name", "email"]
            },
            "UserRegister": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Nombre completo del usuario"},
                    "email": {"type": "string", "format": "email", "description": "Email del usuario"},
                    "password": {"type": "string", "format": "password", "description": "Contraseña (mínimo 6 caracteres)"}
                },
                "required": ["name", "email", "password"]
            },
            "UserUpdate": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Nuevo nombre del usuario"},
                    "email": {"type": "string", "format": "email", "description": "Nuevo email del usuario"},
                    "password": {"type": "string", "format": "password", "description": "Nueva contraseña (opcional)"}
                }
            },
            "UserLogin": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "format": "email", "description": "Email registrado"},
                    "password": {"type": "string", "format": "password", "description": "Contraseña"}
                },
                "required": ["email", "password"]
            }
        }
    })
    
if __name__ == '__main__':
    app.run(debug=True)