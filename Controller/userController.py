from Models.User import User
from flask import jsonify
from flask_jwt_extended import create_access_token

def get_all_users():
    """Obtener todos los usuarios"""
    try:
        users = User.get_all()
        return users, 200
    except Exception as error:
        print(f"ERROR: {error}")
        return {'msg': 'Error al obtener los usuarios'}, 500
    
def create_user(name, email, password):
    """Crear un nuevo usuario"""
    try:
        user_id = User.create(name, email, password)
        user = User.find_by_id(user_id)
        return User.to_dict(user), 201
    except Exception as e:
        print(f"ERROR: {e}")
        return {'msg': 'Error al crear el usuario'}, 500
    
def login_user(email, password):
    """Iniciar sesión"""
    user = User.find_by_email(email)
    if user and User.check_password(user, password):
        access_token = create_access_token(identity=email)
        return {
            'access_token': access_token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email']
            }
        }, 200
    return {'msg': 'Correo o Contraseña incorrectos'}, 401