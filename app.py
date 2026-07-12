from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración JWT
app.config['JWT_SECRET_KEY'] = "hola"
jwt = JWTManager(app)

# Configuración MongoDB
app.config["MONGO_URI"] = os.getenv('DATABASE_URL')
mongo = PyMongo(app)

# Verificar conexión a MongoDB primero
try:
    # Intentar obtener el nombre de la base de datos
    db_name = mongo.db.name
    print(f"Conectado a MongoDB: {db_name}")
    
    # Inicializar el modelo User con la base de datos
    from Models.User import User
    User.init_db(mongo.db)
    
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    print("La aplicación se iniciará sin conexión a la base de datos")
    # Inicializar User con None para evitar errores
    from Models.User import User
    User.init_db(None)

# Configurar Swagger
app.config['SWAGGER'] = {
    'title': 'User API',
    'uiversion': 3,
    'securityDefinitions': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT token. Ejemplo: "Bearer <token>"'
        }
    },
    'security': [
        {'BearerAuth': []}
    ]
}
swagger = Swagger(app)

# Rutas
from Routes.user import user_bp
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)