from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.template.loader import render_to_string

import string
import secrets


class Util:
    @staticmethod
    def send_email(data):
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            message = render_to_string(data['template'], data)

            '''email = EmailMessage(connection=connection)
            email.set_content(message, subtype='html')
            email["Subject"] = data['subject']
            email["From"] = settings.DEFAULT_FROM_EMAIL
            email["To"] = [data['email'], ]
            email.send()'''
            email = EmailMessage(data['subject'], message, settings.DEFAULT_FROM_EMAIL, [
                                 data['email'], ], connection=connection)
            email.content_subtype = "html"
            email.send()

    @staticmethod
    def generate_random_password(length=8):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation

        all = (lower + upper + num + symbols).replace('\'',
                                                      '').replace('"', '').replace('\\', '')

        temp = "".join(secrets.choice(all) for i in range(length))

        return temp
