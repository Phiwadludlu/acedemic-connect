
import os
import threading
from flask import copy_current_request_context, url_for
from itsdangerous import URLSafeTimedSerializer

from models.auth_models.user_model import User


class AuthService:

    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    
  
    def generate_token(self,fs_uniquifier):

        return self.serializer.dumps(fs_uniquifier,salt='abcdasdad213123123')

    def decode_token(self,token,expiration = 600):
       
        try:
            fs_uniquifier = self.serializer.loads(
                token,salt="abcdasdad213123123", max_age=expiration


            )

            return fs_uniquifier

        except Exception as e:
            return None
        
       

    def generate_confimation_link(self, user:User):


        token = self.generate_token(user.fs_uniquifier)

        return url_for("core_routes.confirm_account", token=token, _external=True)
    
    
    def send_confimation_link(self, user:User):

        confimation_link = self.generate_confimation_link(user=user)
        user_email = user.email
        message = f"Hello, thank you for signing up to academic connect please confirm your email, {confimation_link}"

        sender = threading.Thread(name='confimation_sender', target=send_email, args=(message,user_email))
        sender.start()
        
  
         

        



def send_email(message: str, email:str):

    from app import app
    from flask_mailman import EmailMessage

    with app.app_context():

        msg = EmailMessage(
        'Please confirm your account!',
        message,
        'from@example.com',
        [email]
        )
        msg.send()

       


