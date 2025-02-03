from mailersend import emails

mailer = emails.NewEmail()

def send_email_request(new_request):
    # define an empty dict to populate with mail values
    mail_body = {}
    mail_from = {
        "name": "KYC check",
        "email": "info@dtcch-2025-db.sibnick.men",
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