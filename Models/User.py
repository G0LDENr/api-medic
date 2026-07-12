from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import datetime

class User:
    # Variable de clase para la base de datos
    db = None
    collection = None
    
    @classmethod
    def init_db(cls, database):
        """Inicializar la base de datos"""
        cls.db = database
        if database is not None:
            cls.collection = database['users']
        else:
            cls.collection = None
            print("Colección de usuarios no disponible")
    
    @classmethod
    def create(cls, name, email, password):
        """Crear un nuevo usuario"""
        if cls.collection is None:
            raise Exception("Base de datos no disponible")
            
        user_data = {
            'name': name,
            'email': email,
            'password': generate_password_hash(password),
            'created_at': datetime.datetime.utcnow(),
            'updated_at': datetime.datetime.utcnow()
        }
        result = cls.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    @classmethod
    def find_by_email(cls, email):
        """Buscar usuario por email"""
        if cls.collection is None:
            return None
        return cls.collection.find_one({'email': email})
    
    @classmethod
    def find_by_id(cls, user_id):
        """Buscar usuario por ID"""
        if cls.collection is None:
            return None
        return cls.collection.find_one({'_id': ObjectId(user_id)})
    
    @classmethod
    def get_all(cls):
        """Obtener todos los usuarios"""
        if cls.collection is None:
            return []
        users = cls.collection.find()
        return [cls.to_dict(user) for user in users]
    
    @classmethod
    def to_dict(cls, user):
        """Convertir documento de MongoDB a diccionario"""
        return {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'created_at': user.get('created_at'),
            'updated_at': user.get('updated_at')
        }
    
    @classmethod
    def check_password(cls, user, password):
        """Verificar contraseña"""
        return check_password_hash(user['password'], password)