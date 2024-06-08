from .Controller import ControllerClass as C

from flask import jsonify, request
from ..models.dataclass import Utilisateur
from .. import app
from .. import db
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
class UserController:

    def getUserUUID(self, email):
        listUser = db.session.query(Utilisateur).filter(Utilisateur.email == email).first()
        if listUser:
            return listUser.uuidUser
        else:
            return None

    def getUserId(self, email):
        listUser = db.session.query(Utilisateur).filter(Utilisateur.email == email).first()
        if listUser:
            return listUser.idUser
        else:
            return None

    def getUserInfo(self, email):
        listUser = db.session.query(Utilisateur).filter(Utilisateur.email == email).first()
        if listUser:
            return jsonify(
                {
                    "status": "success",
                    "message": "User found",
                    "username": listUser.username,
                    "email": listUser.email,
                    "isAdmin": listUser.isAdmin
                }
            )
        else:
            return jsonify({"status": "failed", "message": "User not found"})



User = UserController()


@app.route("/user/getuuid", methods=['POST'])
@jwt_required()
def getUUID():
    paramettre = C.parametersissetPOST(['email'], request.json)
    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})
    email = request.json.get('email', None)
    useremail = get_jwt_identity()
    if email != useremail:
        return jsonify({"status": "failed", "message": "Invalid email"})

    if email:
        res = User.getUserUUID(email)
        return jsonify({"status": "success", "uuid": res})
    else:
        return jsonify({"status": "failed", "message": "Invalid email"})

@app.route("/user/getinfo", methods=['POST'])
@jwt_required()
def getUserInfo():

    paramettre = C.parametersissetPOST(['email'], request.json)
    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})

    email = request.json.get('email', None)

    useremail = get_jwt_identity()
    if email != useremail:
        return jsonify({"status": "failed", "message": "Invalid email"})

    if email:
        return User.getUserInfo(email)
    else:
        return jsonify({"status": "failed", "message": "Invalid email"})