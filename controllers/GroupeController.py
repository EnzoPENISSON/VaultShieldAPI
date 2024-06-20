from datetime import datetime, timedelta

from .Controller import ControllerClass as C

from flask import jsonify, request
from ..models.dataclass import Groupe, Partager, Coffre, sharegroupe_users
from .utilitytool import UtilityTool
from .. import app
from .. import db
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt


class GroupeController:
    tool = UtilityTool()
    def ajouterGroup(self, uuidUser, nomGroup):
        try:
            group = Groupe(
                uuidGroupe=self.tool.longUUIDGenerator(),
                uuidUserCreator=uuidUser,
                Nom=nomGroup
            )
            if not db.session.query(Groupe).filter(Groupe.Nom == nomGroup).first():
                db.session.add(group)
                db.session.commit()
            return jsonify({"status": "success", "message": "Group added"})

        except Exception as e:

            return jsonify({"status": "failed", "message": "Error adding group "+str(e)})

    def getListsGroups(self, uuidUser):
        try:
            groupscreate = db.session.query(Groupe).filter(Groupe.uuidUserCreator == uuidUser).all()
            groupshare = db.session.query(Groupe).join(sharegroupe_users).filter(sharegroupe_users.uuidUser == uuidUser).all()
            groups_list = []
            for group in groupscreate:
                groups_list.append(
                    {
                        "uuidGroupe": group.uuidGroupe,
                        "Nom": group.Nom
                    }
                )
            for group in groupshare:
                groups_list.append(
                    {
                        "uuidGroupe": group.uuidGroupe,
                        "Nom": group.Nom
                    }
                )
            # remove duplicate
            groups_list = [dict(t) for t in {tuple(d.items()) for d in groups_list}]
            return jsonify({"status": "success", "groups": groups_list})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error getting groups "+str(e)})

    def sharegroupUser(self,uuidUserRequest, emailusershare, uuidGroup,isExpired):

        try:
            uuiidentifiant = self.tool.getUserUUID(emailusershare)
            # group is created by the user
            if not db.session.query(Groupe).filter(Groupe.uuidGroupe == uuidGroup, Groupe.uuidUserCreator == uuidUserRequest).first():
                return jsonify({"status": "failed", "message": "Group not found"})

            if uuiidentifiant == uuidUserRequest:
                return jsonify({"status": "failed", "message": "Invalid user"})


            isExpired = datetime.now() + timedelta(days=1) if isExpired == 1 else None
            sharegroup = sharegroupe_users(
                uuidUser=uuiidentifiant,
                uuidGroupe=uuidGroup,
                Shared_Time=datetime.now(),
                Expired_Time=isExpired
            )
            db.session.add(sharegroup)
            db.session.commit()
            return jsonify({"status": "success", "message": "Group shared"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error sharing group "+str(e)})

group = GroupeController()
@app.route("/group/add", methods=['POST'])
@jwt_required()
def addGroup():
    try:
        uuiduser = get_jwt_identity()

        return group.ajouterGroup(uuiduser, request.json.get('nomGroup'))
    except Exception as e:
        return jsonify({"status": "failed", "message": "Error adding group "+str(e)})

@app.route("/group/list", methods=['GET'])
@jwt_required()
def listGroups():
    try:
        uuidUser = get_jwt_identity()

        return group.getListsGroups(uuidUser)
    except Exception as e:
        return jsonify({"status": "failed", "message": "Error getting groups "+str(e)})



@app.route("/group/share", methods=['POST'])
@jwt_required()
def shareGrouptoUser():
    try:
        uuidusercreator = get_jwt_identity()
        paramettre = C.parametersissetPOST(['uuidGroup','isExpired','emailusershare'], request.json)
        if not paramettre:
            return jsonify({"status": "failed", "message": "Missing parameters"})


        uuidGroup = request.json.get('uuidGroup', None)
        emailusershare = request.json.get('emailusershare', None)
        isExpired = request.json.get('isExpired', 0)

        return group.sharegroupUser(uuidusercreator,emailusershare, uuidGroup, isExpired)
    except Exception as e:
        return jsonify({"status": "failed", "message": "Error sharing password "+str(e)})