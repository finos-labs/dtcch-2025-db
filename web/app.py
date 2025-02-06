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

# Folder to save uploaded files
UPLOAD_FOLDER = '/home/ubuntu/data/kyc/uploads'
KYC_RUN_SCRIPT = '/home/ubuntu/dtcch-2025-db/llm_agent_workflows/main.py'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'jpg', 'png', 'jpeg'}
app.config['KYC_RUN'] = os.environ.get('KYC_RUN', 'test/kyc_script.py')
app.config['POLICY_RUN'] = os.environ.get('POLICY_RUN', 'test/policy_script.py')

if __name__ == '__main__':
    from api import *
    app.run(debug=True)