from flask import Blueprint, request, jsonify
from controllers.userController import (
    get_all_users, 
    get_user_by_id, 
    register_user, 
    update_user, 
    delete_user,
    login_user
)
from werkzeug.security import check_password_hash

user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Obtener todos los usuarios registrados"""
    users = get_all_users()
    return jsonify(users)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obtener un usuario específico por ID"""
    user = get_user_by_id(user_id)
    return jsonify(user)

@user_bp.route('/register', methods=['POST'])
def register():
    """Registrar un nuevo usuario"""
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400
    
    new_user = register_user(data)
    return jsonify(new_user), 201

@user_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión con email y contraseña"""
    try:
        # 1. Validar datos de entrada
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid JSON data",
                "status": 400
            }), 400

        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email or not password:
            return jsonify({
                "success": False,
                "error": "Email and password are required",
                "status": 400
            }), 400

        # 2. Debug: Mostrar datos recibidos
        print(f"Login attempt - Email: {email}, Password: {password}")

        # 3. Autenticar usuario
        user_data = login_user(email, password)
        
        if not user_data:
            print("Login failed - Invalid credentials")
            return jsonify({
                "success": False,
                "error": "Invalid email or password",
                "status": 401
            }), 401

        # 4. Debug: Login exitoso
        print(f"Login successful for user: {user_data['email']}")

        # 5. Respuesta exitosa
        return jsonify({
            "success": True,
            "user": {
                "id": user_data["id"],
                "name": user_data["name"],
                "email": user_data["email"]
            },
            "message": "Login successful",
            "status": 200
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "status": 500
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update(user_id):
    """Actualizar información de usuario"""
    data = request.json
    user = update_user(user_id, data)
    return jsonify(user)

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    """Eliminar un usuario"""
    response = delete_user(user_id)
    return jsonify(response)