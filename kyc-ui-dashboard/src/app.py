from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, expose_headers=["Authorization"])
app.config["JWT_SECRET_KEY"] = "supersecretkey"  # Change this in production

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Simulated user database
users = {
    "admin": {
        "password": bcrypt.generate_password_hash("password").decode("utf-8"),
        "email": "john@example.com",
        "department": "Compliance",
        "avatar": "https://i.pravatar.cc/100"
    }
}

clients = ["Client A", "Client B", "Client C"]
policies = ["Policy X", "Policy Y", "Policy Z"]

kyc_requests = [
            {"id": "KYC001", "clientName": "Alice Smith", "policy": "Policy A", "triggerDate": "2024-02-01", "status": "Pending"},
            {"id": "KYC002", "clientName": "Bob Johnson", "policy": "Policy B", "triggerDate": "2024-02-02", "status": "Approved"},
            {"id": "KYC003", "clientName": "Charlie Brown", "policy": "Policy C", "triggerDate": "2024-02-03", "status": "Rejected"},
        ]


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
    
# ==========================
# 📌 KYC Requests
# ==========================
@app.route("/kyc_requests", methods=["GET", "POST"])
@jwt_required()
def handle_kyc_requests():
    email = get_jwt_identity()

    if request.method == "GET":
        return jsonify(kyc_requests), 200

    elif request.method == "POST":
        data = request.json
        client, policy = data.get("client"), data.get("policy")

        if not client or not policy:
            return jsonify({"error": "Client and Policy are required"}), 400

        new_request = {
            "id": f"KYC{len(kyc_requests) + 1:03}",
            "clientName": client,
            "policy": policy,
            "triggerDate": datetime.now().strftime("%Y-%m-%d"),
            "status": "Pending",
        }
        kyc_requests.append(new_request)
        return jsonify({"message": "KYC request submitted", "data": new_request}), 201


@app.route("/clients", methods=["GET"])
def get_clients():
    try:
        print("Fetching clients")

        # Simulated clients (Replace this with actual database logic)
        clients = ["Alice Smith", "Bob Johnson", "Charlie Brown"]

        return jsonify(clients), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/policies", methods=["GET"])
def get_policies():
    try:
        print(f"Fetching policies")

        # Simulated KYC requests (Replace this with actual database logic)
        polices = ["Policy A", "Policy B", "Policy C"]

        return jsonify(polices), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/kyc_requests", methods=["POST"])
@jwt_required()
def trigger_kyc():
    data = request.json
    client, policy = data.get("client"), data.get("policy")

    if not client or not policy:
        return jsonify({"error": "Client and Policy are required"}), 400

    new_request = {
        "id": f"KYC{len(kyc_requests) + 1:03}",
        "clientName": client,
        "policy": policy,
        "triggerDate": datetime.now().strftime("%Y-%m-%d"),
        "status": "Pending",
    }
    kyc_requests.append(new_request)
    return jsonify({"message": "KYC request successfully submitted", "data": new_request}), 201


# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
