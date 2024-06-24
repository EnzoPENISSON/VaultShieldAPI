import json
from datetime import datetime, timedelta
from .Controller import ControllerClass as C
from flask import jsonify, request, session
from ..models.dataclass import Utilisateur
from .. import app
from .. import db
import bcrypt
from .utilitytool import UtilityTool
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from .EmailSender import EmailSender
from .. import mail



class Authentification:
    tool = UtilityTool()
    mailer = EmailSender(mail)

    def login(self, email, password):
        listUser = db.session.query(Utilisateur).filter(Utilisateur.email == email)

        for user in listUser:
            enc_pw = user.password.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), enc_pw):
                # Create access and refresh tokens with expiration time
                access_token = create_access_token(identity=user.uuidUser)
                # Save tokens into the database
                user.token = access_token
                user.last_co = db.func.now()
                db.session.commit()

                return jsonify(
                    {
                        "status": "success",
                        "message": "User connected",
                        "username": user.username,
                        "access_token": access_token
                    }
                )

        return jsonify({"status": "failed", "message": "Invalid email or password"})

    def me(self, uuidUser):
        user = db.session.query(Utilisateur).filter(Utilisateur.uuidUser == uuidUser).first()
        if not user:
            return jsonify({"status": "failed", "message": "User not found"})

        return jsonify(
            {
                "status": "success",
                "username": user.username,
                "email": user.email,
            }
        )
    def register(self, email, password, username):
        try:
            hashed_pw = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
            new_user = Utilisateur(
                uuidUser=self.tool.longUUIDGenerator(),
                email=email,
                password=hashed_pw,
                username=username
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(
                    {
                        "status": "success",
                        "message": "User created"
                    }
                )
        except Exception as e:
            print(e)
            return jsonify(
                    {
                        "status": "error",
                        "message": "User creation failed"
                    }
                )

    def reset_password(self, email):
        user = db.session.query(Utilisateur).filter(Utilisateur.email == email).first()
        if not user:
            return jsonify({"status": "failed", "message": "User not found"})

        # Generate a new OTP
        otp = self.tool.generate_otp()
        user.OTP_code = otp
        user.OTP_expired = datetime.now() + timedelta(minutes=5)
        db.session.commit()

        # Send the OTP to the user's email
        self.mailer.send_otp(email, 'Code de verification', otp)

        return jsonify({"status": "success", "message": "OTP sent to your email"})

    def verify_otp(self, email, otp):
        user = db.session.query(Utilisateur).filter(Utilisateur.email == email).first()
        if not user:
            return jsonify({"status": "failed", "message": "User not found"})

        # Check if the OTP is valid
        if user.OTP_code == otp and user.OTP_expired > datetime.now():
            reset_token = self.tool.longUUIDGenerator() + "-" + self.tool.longUUIDGenerator()
            reset_token_expiry = datetime.now() + timedelta(hours=1)
            user.reset_token = reset_token
            user.reset_token_expiry = reset_token_expiry
            db.session.commit()

            return jsonify({"status": "success", "message": "OTP is valid", "urlreset": reset_token})
        else:
            return jsonify({"status": "failed", "message": "Invalid OTP"})

    def change_password(self, reset_token, password, password_confirmation):
        if password != password_confirmation:
            return jsonify({"status": "failed", "message": "Passwords do not match"})

        new_password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

        if len(new_password) < 12 and not any(char.isdigit() for char in new_password):
            return jsonify({"status": "failed", "message": "Password too short (12 characters minimum) and must contain at least one digit"})

        user = db.session.query(Utilisateur).filter(Utilisateur.reset_token == reset_token).first()

        if not user or user.reset_token_expiry < datetime.now():
            return jsonify({"status": "failed", "message": "Invalid or expired reset token"})

        # Update the user's password
        user.password = new_password  # You should hash the password before storing it
        user.reset_token = None
        user.reset_token_expiry = None
        user.OTP_code = None
        user.OTP_expired = None
        db.session.commit()

        return jsonify({"status": "success", "message": "Password has been reset successfully"})


auth = Authentification()

@app.route("/auth/login", methods=['POST'])
def login():
    paramettre = C.parametersissetPOST(['email','password'], request.json)
    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})

    req_data = request.get_json(force=True)

    return auth.login(req_data['email'],req_data['password'])

@app.route("/auth/register", methods=['POST'])
def register():
    req_data = request.get_json(force=True)

    # control it fit is an email
    if '@' not in req_data['email'] or '.' not in req_data['email']:
        return json.dumps({"status": "failed", "message": "Invalid email"})

    # control if the password is empty or shorter than 12 characters
    if len(req_data['password']) < 12:
        return jsonify({"status": "failed", "message": "Password too short (12 characters minimum)"})


    return auth.register(req_data['email'],req_data['password'],req_data['username'])

@app.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()

    # Update the token in the database
    user = db.session.query(Utilisateur).filter(Utilisateur.email == current_user).first()
    user.token = None
    user.token_refresh = None
    user.token_refresh_exp = None
    db.session.commit()

    return jsonify(message="User logged out"), 200  # Respond with the new access token

@app.route('/auth/reset_password', methods=['POST'])
def reset_password():
    paramettre = C.parametersissetPOST(['email'], request.json)
    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})

    req_data = request.get_json(force=True)

    return auth.reset_password(req_data['email'])

@app.route('/auth/verify_otp', methods=['POST'])
def verify_otp():
    paramettre = C.parametersissetPOST(['email', 'otp'], request.json)
    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})

    req_data = request.get_json(force=True)

    return auth.verify_otp(req_data['email'], req_data['otp'])

@app.route('/auth/change_password/<reset_token>', methods=['PUT'])
def change_password(reset_token):
    req_data = request.get_json(force=True)
    new_password = req_data['new_password']
    confirm_password = req_data['confirm_password']


    return auth.change_password(reset_token,new_password, confirm_password)