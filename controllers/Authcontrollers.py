import json
import time
from datetime import timedelta, datetime

from flask import jsonify, request
from ..models.dataclass import Utilisateur
from .. import app
from .. import db
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
class Authentification:

    def login(self, email, password):
        listUser = db.session.query(Utilisateur).filter(Utilisateur.email == email)

        for user in listUser:
            enc_pw = user.password.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), enc_pw):
                # Create access and refresh tokens with expiration time
                access_token = create_access_token(identity=email)
                refresh_token = create_refresh_token(identity=email)

                # Save tokens into the database
                user.token = access_token
                user.token_refresh = refresh_token
                user.token_refresh_exp = datetime.now() + timedelta(hours=7)
                user.last_co = db.func.now()
                db.session.commit()

                return json.dumps(
                    {
                        "status": "success",
                        "message": "User connected",
                        "username": user.username,
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    }
                )

        return json.dumps({"status": "failed", "message": "Invalid email or password"})

    def register(self, email, password, username):
        try:
            hashed_pw = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
            new_user = Utilisateur(email=email, password=hashed_pw, username=username)
            db.session.add(new_user)
            db.session.commit()
            response = app.response_class(
                response=json.dumps(
                    {
                        "status": "success",
                        "message": "User created"
                    }
                ),
                status=200,
                mimetype='application/json'
            )
            return response
        except Exception as e:
            #print(e)
            response = app.response_class(
                response=json.dumps(
                    {
                        "status": "error",
                        "message": "User creation failed"
                    }
                ),
                status=500,
                mimetype='application/json'
            )
            return response

        def send_email(self, email):
            pass
        def reset_password(self, email):
            send_email(email)


auth = Authentification()

@app.route("/auth/login", methods=['POST'])
def login():
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
        return json.dumps({"status": "failed", "message": "Password too short (12 characters minimum)"})


    return auth.register(req_data['email'],req_data['password'],req_data['username'])

@app.route('/auth/me', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token

    return jsonify(logged_in_as=current_user), 200  # Respond with the identity in JSON format

@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token

    # Generate a new access token
    new_access_token = create_access_token(identity=current_user)

    # Update the token in the database
    user = db.session.query(Utilisateur).filter(Utilisateur.email == current_user).first()
    user.token = new_access_token
    db.session.commit()

    return jsonify(access_token=new_access_token), 200  # Respond with the new access token


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