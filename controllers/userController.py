from models.User import User
from config import db
from werkzeug.security import generate_password_hash, check_password_hash

def get_all_users():
    """Obtener todos los usuarios"""
    return [user.to_dict() for user in User.query.all()]

def get_user_by_id(user_id):
    """Obtener usuario por ID"""
    user = User.query.get_or_404(user_id)
    return user.to_dict()

from werkzeug.security import generate_password_hash

def register_user(data):
    """Registro con hashing consistente"""
    if User.query.filter_by(email=data['email']).first():
        return None
    
    try:
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password']  # El modelo se encarga del hashing
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict()
    except Exception as e:
        print(f"Error en registro: {str(e)}")
        db.session.rollback()
        return None

def login_user(email, password):
    """Autenticar usuario"""
    print(f"Buscando usuario: {email}")
    user = User.query.filter_by(email=email).first()
    
    if not user:
        print("Usuario no encontrado")
        return None
    
    print(f"Verificando contraseña para: {user.email}")
    try:
        if user.verify_password(password):
            print("Contraseña válida")
            return user.to_dict()
        else:
            print("Contraseña inválida")
            return None
    except AttributeError as e:
        print(f"Error de atributo: {str(e)}")
        return None


def update_user(user_id, data):
    """Actualizar información de usuario"""
    user = User.query.get_or_404(user_id)
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    db.session.commit()
    return user.to_dict()

def delete_user(user_id):
    """Eliminar usuario"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}