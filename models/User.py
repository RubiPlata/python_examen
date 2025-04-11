from werkzeug.security import generate_password_hash, check_password_hash
from config import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Aumenté el tamaño para hashes largos

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)  # Hashear al crear

    def set_password(self, password):
        """Hashear con parámetros consistentes"""
        self.password_hash = generate_password_hash(
            password,
            method='scrypt',
            salt_length=16
        )

    def verify_password(self, password):
        """Verificación robusta con debug"""
        try:
            result = check_password_hash(self.password_hash, password)
            print(f"Hash almacenado: {self.password_hash}")
            print(f"Contraseña a verificar: {password}")
            print(f"Resultado verificación: {result}")
            return result
        except Exception as e:
            print(f"Error en verify_password: {str(e)}")
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }