import json
import time
from .Controller import ControllerClass as C
from flask import jsonify, request
from ..models.dataclass import Utilisateur
from .. import app
from .. import db
import bcrypt
from .tools import Tools
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
class Authentification:
    tool = Tools()

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

        def send_email(self, email):
            pass
        def reset_password(self, email):
            send_email(email)


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

@app.route('/auth/me', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token


    return auth.me(current_user)

@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=False)
def refresh_token():
    current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token

    # Check if the access token is expired
    token_is_expired = get_jwt()['exp'] < time.time()

    if token_is_expired:
        # Check if the refresh token is expired
        return jsonify(
            success=False,
            message="Access token is expired. Please reconnect."
        ), 401
    else:
        temps = (get_jwt()['exp'] - time.time()) / 60
        # convert the time in seconds to minutes
        return jsonify(
            success=True,
            message="Access token is not expired. No need to refresh.",
        ), 200


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