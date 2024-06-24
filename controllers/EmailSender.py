from flask import render_template
from flask import jsonify, request, session
from .utilitytool import UtilityTool
from .. import Message


class EmailSender:
    def __init__(self, mail):
        self.mail = mail
        self.tool = UtilityTool()

    def send_email(self, email, subject, message_type='otp', custom_message=None, element=None):
        otp = element if message_type == 'otp' else None
        session['otp'] = otp

        msg = Message(subject,
                      sender='noreply.vaultshield@gmail.com',
                      recipients=[email])

        if message_type == 'otp':
            # use template in tamplates folder
            html_content = render_template('email_template.html', otp=otp)
            msg.html = html_content
        elif custom_message:
            msg.body = custom_message

        self.mail.send(msg)

        return jsonify({"status": "success", "message": f"{message_type.capitalize()} sent to your email"})

    def send_otp(self, email,messagecontenttype, otp=None):
        return self.send_email(email, messagecontenttype, element=otp)
