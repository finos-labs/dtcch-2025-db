from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager
)
from flask_bcrypt import Bcrypt

import os

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dtcch:mypassword@localhost:5432/dtcch'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, expose_headers=["Authorization"])
app.config["JWT_SECRET_KEY"] = "supersecretkey"  # Change this in production

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Simulated user database
users = {
    "admin": {
        "id": 1,
        "password": bcrypt.generate_password_hash("password").decode("utf-8"),
        "email": "john@example.com",
        "department": "Compliance",
        "avatar": "https://i.pravatar.cc/100"
    }
}

# Folder to save uploaded files
UPLOAD_FOLDER = '/home/ubuntu/data/kyc/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'jpg', 'png', 'jpeg'}

if __name__ == '__main__':
    from api import *
    app.run(debug=True)