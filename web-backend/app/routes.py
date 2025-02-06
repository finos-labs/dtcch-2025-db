# app/routes.py
from flask import Blueprint
from flask import Flask, request, jsonify
import os

if 'HOME' in os.environ:
    UPLOAD_FOLDER = os.environ['HOME'] + '/uploads/'
else: UPLOAD_FOLDER = "uploads/"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

main_routes = Blueprint('main', __name__)
client_doc_types = sorted([
    "Utility Bill",
    "Bank statement",
    "Council tax letter",
    "Driving licence",
    "Document issued by public sector or local authority",
    "Constitutional document",
    "Document from independent lawyer or accountant",
    "Directors list",
    "Notarised Ownership chart",
    "Government Issued photo ID",
    "Passport"
])

@main_routes.route('/request_doc_types/<uid>', methods=['GET'])
def request_doc_types(uid):
    from . import db
    from .models import RequestForDocs

    #rs = client_doc_types[0:3]
    print(uid)
    user = db.session.query(RequestForDocs).filter_by(string_id=uid).first()
    print(user)
    return user.doc_types

@main_routes.route('/request_docs', methods=['POST'])
def request_docs():
    from . import db
    from .models import RequestForDocs

    data = request.get_json()

    if (not data or 'email_text' not in data or 'email' not in data or 'callback_url' not in data
            or 'string_id' not in data or 'doc_types' not in data):
        return jsonify({'error': 'Missing required fields'}), 400

    email = data['email']
    email_text = data['email_text']
    callback_url = data['callback_url']
    string_id = data['string_id']
    import json
    doc_types = json.dumps(data['doc_types'])
    print(doc_types)
    try:
        # Create a new RequestForDocs object
        new_request = RequestForDocs(
            email=email,
            email_text=email_text,
            callback_url=callback_url,
            string_id=string_id,
            doc_types=doc_types
        )

        # Add and commit the new request to the database
        db.session.add(new_request)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.commit()

    from .email_service import send_email_request
    send_email_request(new_request)

    return jsonify({'message': 'Request stored successfully'}), 201



@main_routes.route('/upload', methods=['POST'])
def upload_files():
    import os
    """Endpoint to handle multiple file uploads."""
    user_hash = request.form.get("uid")
    print(user_hash)
    files = {}

    for doc_type in client_doc_types:
        files_pro_type = request.files.getlist(doc_type)
        if files_pro_type:
            files[doc_type] = files_pro_type

    if len(files) == 0:
        return jsonify({"error": "No files part in the request"}), 400

    uploaded_files = []
    upload_folder = os.path.join(UPLOAD_FOLDER, user_hash)
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    for file_type in files.keys():
        file_type_dir = os.path.join(upload_folder, file_type)
        if not os.path.exists(file_type_dir):
            os.makedirs(file_type_dir)
    to_process = {}
    for file_type, files_pro_type in files.items():
        to_process[file_type] = []
        for file in files_pro_type:
            if file.filename == '':
                continue
            if file:
                filename = file.filename
                file_path = os.path.join(upload_folder, file_type, filename)
                file.save(file_path)
                uploaded_files.append(filename)
                to_process[file_type].append(file_path)
            else:
                return jsonify({"error": f"File type not allowed: {file.filename}"}), 400

    from .data_extractor import process_files
    process_files(user_hash, files)
    #return jsonify({"message": "Files uploaded successfully", "uploaded_files": uploaded_files}), 200
    return "<h1>Files Uploaded Successfully!</h1>", 200

