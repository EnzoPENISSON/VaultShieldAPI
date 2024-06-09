from .Controller import ControllerClass as C

from flask import jsonify, request
from ..models.dataclass import Groupe
from .tools import Tools
from .. import app
from .. import db
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt


class GroupeController:
    def ajouterGroup(self, idUser, nomGroup):
        try:
            group = Groupe(
                idUser=idUser,
                Nom=nomGroup
            )
            if not db.session.query(Groupe).filter(Groupe.Nom == nomGroup).first():
                db.session.add(group)
                db.session.commit()
            return jsonify({"status": "success", "message": "Group added"})

        except Exception as e:

            return jsonify({"status": "failed", "message": "Error adding group "+str(e)})


group = GroupeController()
@app.route("/group/add", methods=['POST'])
@jwt_required()
def addGroup():
    try:
        useremail = get_jwt_identity()

        user = Tools()
        res = user.userExist(useremail, request.json)
        if res:
            return res

        userid = user.getUserId(useremail)

        return group.ajouterGroup(userid, request.json.get('nomGroup'))
    except Exception as e:
        return jsonify({"status": "failed", "message": "Error adding group "+str(e)})