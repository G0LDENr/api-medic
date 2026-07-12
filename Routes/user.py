from flask import Blueprint, request, jsonify
from Controller.userController import get_all_users, create_user, login_user
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def index():
    """
    Obtener todos los usuarios
    ---
    responses:
      200:
        description: Lista de usuarios
    """
    data, status_code = get_all_users()
    return jsonify(data), status_code

@user_bp.route('/add_user', methods=['POST'])
@jwt_required()
def user_store():
    """
    Crear un nuevo usuario (Requiere autenticación)
    ---
    tags:
      - Usuarios
    security:
      - BearerAuth: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - name
            - password
          properties:
            email:
              type: string
            name:
              type: string
            password:
              type: string
    responses:
      201:
        description: Usuario creado correctamente
      400:
        description: Datos inválidos o incompletos
      401:
        description: Token inválido o no proporcionado
    """
    current_user_email = get_jwt_identity()
    print(f"Usuario autenticado: {current_user_email}")
    
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'No data provided'}), 400
    
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    if not email or not name or not password:
        return jsonify({'msg': 'todos los campos son obligatorios'}), 400
    
    data, status_code = create_user(name, email, password)
    return jsonify(data), status_code

@user_bp.route('/login', methods=['POST'])
def login():
    """
    Iniciar sesión de usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Sesión iniciada exitosamente
      400:
        description: Datos incompletos o inválidos
      401:
        description: Credenciales incorrectas
    """
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'el cuerpo de la solicitud debe ser JSON'}), 400
    
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'msg': 'Correo y Contraseña son obligatorios'}), 400
    
    data, status_code = login_user(email, password)
    return jsonify(data), status_code