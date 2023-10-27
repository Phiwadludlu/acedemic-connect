import threading
from flask import copy_current_request_context
from flask_security import MailUtil

from flask_mailman import EmailMultiAlternatives, Mail

mail = Mail()

class MyMailUtil(MailUtil):

    def send_mail(self, template, subject, recipient, sender, body, html, **kwargs):
        
        send_flask_mail(
            subject=subject,
            from_email=sender,
            to=[recipient],
            body=body,
            html=html,
            )

      
def send_flask_mail(**kwargs):
    from app import app
    with app.app_context():
        with mail.get_connection() as connection:
            html = kwargs.pop("html", None)
            msg = EmailMultiAlternatives(**kwargs, connection=connection)
            if html:
                msg.attach_alternative(html, "text/html")
            msg.send()