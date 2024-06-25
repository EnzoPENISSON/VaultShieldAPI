from .Controller import ControllerClass as C

from flask import jsonify, request
from ..models.dataclass import Utilisateur
from .. import app
from .. import db
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
class UserController:

    def getUserUUID(self, email):
        try:
            listUser = db.session.query(Utilisateur).filter(Utilisateur.email == email).first()
            if listUser:
                return listUser.uuidUser
            else:
                return None
        except Exception as e:
            return None

    def getUserInfo(self, uuiduser):
        try:
            listUser = db.session.query(Utilisateur).filter(Utilisateur.uuidUser == uuiduser).first()
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
        except Exception as e:
            return jsonify({"status": "failed", "message": "User not found"})



User = UserController()


@app.route("/user/getuuid", methods=['POST'])
@jwt_required()
def getUUID():
    uuiduser = get_jwt_identity()

    if uuiduser is not None:
        return jsonify({"status": "success", "uuid": uuiduser})
    else:
        return jsonify({"status": "failed", "message": "Invalid email"})

@app.route("/user/getinfo", methods=['POST'])
@jwt_required()
def getUserInfo():

    uuiduser = get_jwt_identity()
    if uuiduser is not None:
        return User.getUserInfo(uuiduser)
    else:
        return jsonify({"status": "failed", "message": "Invalid email"})