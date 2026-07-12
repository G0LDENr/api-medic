import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Conexión a MongoDB
MONGO_URI = os.getenv('DATABASE_URL')
client = MongoClient(MONGO_URI)
db = client.get_database()