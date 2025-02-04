from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dtcch:mypassword@localhost/dtcch'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the REQUEST_FOR_DOCS model
class RequestForDocs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_text = db.Column(db.Text, nullable=False)
    callback_url = db.Column(db.Text, nullable=False)
    string_id = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


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

if __name__ == '__main__':
    app.run(debug=True)