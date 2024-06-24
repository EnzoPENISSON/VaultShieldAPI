import json
import random
from datetime import datetime, timedelta
from .Controller import ControllerClass as C
from flask import jsonify, request, session
from ..models.dataclass import Utilisateur, Coffre
from .. import app
from .. import db
import bcrypt
from .utilitytool import UtilityTool
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from .EmailSender import EmailSender
from .. import mail


class AdminControllers:
    tool = UtilityTool()
    def isUserAdmin(self, uuidUser):
        user = db.session.query(Utilisateur).filter(Utilisateur.uuidUser == uuidUser).first()
        if user.isAdmin == 1:
            return True
        else:
            return False

    def listAdmin(self,uuidUser):
        # if uuiduser not admin return failed
        if self.isUserAdmin(uuidUser) == False:
            return jsonify({"status": "failed", "message": "User is not admin"})

        users = db.session.query(Utilisateur).filter(Utilisateur.isAdmin == 1).all()
        users_list = []
        for user in users:
            users_list.append(
                {
                    "username": user.username,
                    "email": user.email,
                }
            )

        return jsonify({"status": "success", "users": users_list})

    def setUserAdmin(self, uuidUser, email):
        if self.isUserAdmin(uuidUser) == False:
            return jsonify({"status": "failed", "message": "User is not admin"})

        user = db.session.query(Utilisateur).filter(Utilisateur.email == email).first()
        if not user:
            return jsonify({"status": "failed", "message": "User not found"})

        user.isAdmin = 1
        db.session.commit()

        return jsonify({"status": "success", "message": "User is now admin"})

    def listeAllVault(self,uuidUser):
        if self.isUserAdmin(uuidUser) == False:
            return jsonify({"status": "failed", "message": "User is not admin"})

        coffres = db.session.query(Coffre).all()
        coffres_list = []
        for coffre in coffres:
            coffres_list.append(
                {
                    "username": self.tool.generate_random_string(),
                    "password": self.tool.generate_random_string(),
                    "urlsite": coffre.urlsite,
                    "urllogo": coffre.urllogo,
                }
            )

        return jsonify({"status": "success", "coffres": coffres_list})


admin = AdminControllers()

@app.route('/admin/listadmin', methods=['GET'])
@jwt_required()
def listadmin():
    uuidUser = get_jwt_identity()
    return admin.listAdmin(uuidUser)

@app.route('/admin/setadmin', methods=['PUT'])
@jwt_required()
def setadmin():
    uuidUser = get_jwt_identity()

    return admin.setUserAdmin(uuidUser, request.json.get('email'))

@app.route('/admin/listvault', methods=['GET'])
@jwt_required()
def listvault():
    uuidUser = get_jwt_identity()

    return admin.listeAllVault(uuidUser)