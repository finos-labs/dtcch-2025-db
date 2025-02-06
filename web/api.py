import logging
from flask import request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_bcrypt import Bcrypt

from data import *
from app import app, db

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

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

def send_email_request(new_request):
    pass
    # from mailersend import emails
    # # assigning NewEmail() without params defaults to MAILERSEND_API_KEY env var
    # mailer = emails.NewEmail()
    # # define an empty dict to populate with mail values
    # mail_body = {}
    # mail_from = {
    #     "name": "KYC check",
    #     "email": "info@trial-z86org8q66zgew13.mlsender.net",
    # }
    # recipients = [
    #     {
    #         "name": "Y  our Client",
    #         "email": "your@client.com",
    #     }
    # ]
    # mailer.set_mail_from(mail_from, mail_body)
    # mailer.set_mail_to(recipients, mail_body)
    # mailer.set_subject("Hello!", mail_body)
    # mailer.set_html_content("This is the HTML content", mail_body)
    # mailer.set_plaintext_content("This is the text content", mail_body)
    # mailer.set_reply_to(reply_to, mail_body)
    #
    # # using print() will also return status code and data
    # mailer.send(mail_body)


@app.route('/request_docs', methods=['POST'])
def request_docs():
    data = request.get_json()

    if not data or 'email_text' not in data or 'callback_url' not in data or 'string_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    email_text = data['email']
    email_text = data['email_text']
    callback_url = data['callback_url']
    string_id = data['string_id']

    try:
        # Create a new RequestForDocs object
        new_request = RequestForDocs(
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

    if username in users and bcrypt.check_password_hash(users[username]["password"], password):
        access_token = create_access_token(identity=username)
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
def actions_list(kyc_id):
    try:
        return jsonify(Actions.query.filter(Actions.kyc_id == kyc_id).all())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
