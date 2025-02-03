# app/routes.py
from flask import Blueprint
from flask import Flask, request, jsonify
main_routes = Blueprint('main', __name__)


@main_routes.route('/request_docs', methods=['POST'])
def request_docs():
    from . import db
    from models import RequestForDocs

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

    from web.app.email_service import send_email_request
    send_email_request(new_request)

    return jsonify({'message': 'Request stored successfully'}), 201
