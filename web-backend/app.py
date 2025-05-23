from dataclasses import dataclass

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from datetime import datetime
from dotenv import load_dotenv
import os

from sqlalchemy.orm import Session

from model.data import Kyc, Ops
load_dotenv()
from mailersend import emails
mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))
from model.data import Kyc

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

# Define the REQUEST_FOR_DOCS model
class RequestForDocs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    email_text = db.Column(db.Text, nullable=False)
    callback_url = db.Column(db.Text, nullable=False)
    string_id = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@dataclass
class Client(db.Model):
    client_id: int = db.Column(db.Integer, primary_key=True)
    client_name: str = db.Column(db.String(255), nullable=False)
    # client_email = db.Column(db.String(255), nullable=False)

class KycProcess(db.Model):
    kyc_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.policy_id'), nullable=False)
    ops_id = db.Column(db.Integer, db.ForeignKey('kyc_ops.ops_id'), nullable=False)
    initiation_timestamp  = db.Column(db.DateTime, nullable=False)
    overall_status = db.Column(db.String(50), nullable=False)

@dataclass
class Actions(db.Model):
    kyc_id: int = db.Column(db.Integer, db.ForeignKey('kyc_process.kyc_id'), primary_key=True)
    latest_action_activity: str = db.Column(db.String(50), nullable=False)
    business_type: str = db.Column(db.ARRAY(db.String))
    due_diligence_level: str = db.Column(db.ARRAY(db.String))
    entity_type: str = db.Column(db.ARRAY(db.String))
    role: str = db.Column(db.ARRAY(db.String))
    policy_quote: str = db.Column(db.Text)
    internal_evidence_source: list = db.Column(db.ARRAY(db.String))
    external_evidence_source: list = db.Column(db.ARRAY(db.String))
    client_evidence_source: list = db.Column(db.ARRAY(db.String))
    data_point: str = db.Column(db.String(255))
    action_description: str = db.Column(db.Text)

@dataclass
class KycOps(db.Model):
    ops_id: int = db.Column(db.Integer, primary_key=True)
    ops_name: str = db.Column(db.String(255), nullable=False)
    ops_designation: str = db.Column(db.String(255), nullable=False)

@dataclass
class Policy(db.Model):
    policy_id: int = db.Column(db.Integer, primary_key=True)
    policy_name: str = db.Column(db.String(255), nullable=False)
    policy_version: str = db.Column(db.String(50), nullable=False)

def send_email_request(new_request):
    # define an empty dict to populate with mail values
    mail_body = {}
    mail_from = {
        "name": "KYC check",
        "email": "info@trial-z86org8q66zgew13.mlsender.net",
    }
    recipients = [
        {
            "name": "KYC Client",
            "email": new_request.email,
        }
    ]
    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("KYC check - please provide documents", mail_body)
    mailer.set_plaintext_content(new_request.email_text, mail_body)

    # using print() will also return status code and data
    mailer.send(mail_body)


@app.route('/request_docs', methods=['POST'])
def request_docs():
    data = request.get_json()

    if not data or 'email_text' not in data or 'email' not in data or 'callback_url' not in data or 'string_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    email = data['email']
    email_text = data['email_text']
    callback_url = data['callback_url']
    string_id = data['string_id']

    try:
        # Create a new RequestForDocs object
        new_request = RequestForDocs(
            email=email,
            email_text=email_text,
            callback_url=callback_url,
            string_id=string_id
        )

        # Add and commit the new request to the database
        db.session.add(new_request)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.commit()

    send_email_request(new_request)

    return jsonify({'message': 'Request stored successfully'}), 201

# User Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    print('User:', username, 'Password:', password)

    if username in users and bcrypt.check_password_hash(users[username]["password"], password):
        access_token = create_access_token(identity=username)  # ✅ Fix: Ensure identity is a string
        print('Token created:', access_token)
        return jsonify(access_token=access_token)

    print('Failed login')
    return jsonify({"error": "Invalid credentials"}), 401


# User Info API (Protected)
@app.route("/user", methods=["GET"])
@jwt_required()
def user_info():
    try:
        token_header = request.headers.get("Authorization", None)
        print("Authorization Header:", token_header)  # Debugging

        username = get_jwt_identity()  # ✅ Now returns only a string
        print("Current User:", username)

        if username not in users:
            return jsonify({"error": "User not found"}), 404

        return jsonify(users[username])

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 401

@app.route('/ops/<ops_id>', methods=['GET'])
def get_ops_details(ops_id):
    try:
        ops = KycOps.query.get(ops_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if ops:
        return jsonify(ops), 200
    else:
        return jsonify({"error": "Ops not found"}), 404

@app.route('/getKycList', methods=['GET'])
@jwt_required()
def get_kyc_list():
    username = get_jwt_identity()  # ✅ Now returns only a string
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    ops_id = users[username]["id"]
    result = []
    try:
        kyc_processes = (db.session.query(
            KycProcess, Client, Policy
        ).filter(KycProcess.client_id == Client.client_id
        ).filter(KycProcess.policy_id == Policy.policy_id
        ).filter(KycProcess.ops_id == ops_id
        ).all())

        for kyc_process, client, policy in kyc_processes:
            result.append(Kyc(kyc_process.kyc_id,
                           kyc_process.client_id,
                           kyc_process.policy_id,
                           client.client_name,
                           policy.policy_name,
                           kyc_process.initiation_timestamp,
                           kyc_process.overall_status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(result), 200

@app.route('/policies', methods=['GET'])
@jwt_required()
def get_policies_list():
    try:
        return jsonify(Policy.query.all())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clients', methods=['GET'])
@jwt_required()
def get_clients_list():
    try:
        return jsonify(Client.query.all())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/triggerKyc', methods=['POST'])
@jwt_required()
def trigger_kyc():
    data = request.get_json()

    if not data or 'client_id' not in data or 'policy_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    username = get_jwt_identity()
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    ops_id = users[username]["id"]

    try:
        new_kyc = KycProcess(
            client_id=data['client_id'],
            ops_id=ops_id,
            policy_id=data['policy_id'],
            initiation_timestamp=datetime.now(),
            overall_status='NEW'
        )

        db.session.add(new_kyc)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.commit()

    return jsonify(new_kyc.kyc_id), 200

@app.route('/kyc/<kyc_id>', methods=['GET'])
@jwt_required()
def kyc_details(kyc_id):
    try:
        kyc_process, client, policy = (db.session.query(
            KycProcess, Client, Policy
        ).filter(KycProcess.client_id == Client.client_id
        ).filter(KycProcess.policy_id == Policy.policy_id
        ).filter(KycProcess.kyc_id == kyc_id
        ).one())
        return jsonify(Kyc(kyc_process.kyc_id,
                           kyc_process.client_id,
                           kyc_process.policy_id,
                           client.client_name,
                           policy.policy_name,
                           kyc_process.initiation_timestamp,
                           kyc_process.overall_status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/actionsList/<kyc_id>', methods=['GET'])
@jwt_required()
def actions(kyc_id):
    try:
        result = (db.session.query(Actions
        ).filter(Actions.kyc_id == kyc_id
        ).all())
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)