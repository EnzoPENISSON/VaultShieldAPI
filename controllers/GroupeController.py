from datetime import datetime, timedelta

from .Controller import ControllerClass as C

from flask import jsonify, request
from ..models.dataclass import Groupe, Partager, Coffre, sharegroupe_users, tablekeyuser,tablekeygroupe
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
            return jsonify(groups_list)
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error getting groups "+str(e)})

    def listVaultGroup(self, uuidUser, uuidGroup):
        try:
            verifgroupsharetoUser = db.session.query(sharegroupe_users).filter(sharegroupe_users.uuidGroupe == uuidGroup, sharegroupe_users.uuidUser == uuidUser).first()

            if not verifgroupsharetoUser:
                return jsonify({"status": "failed", "message": "Group not found"})

            coffres = db.session.query(Coffre).join(Partager).filter(Partager.uuidGroupe == uuidGroup).all()
            vaults_list = []
            for coffre in coffres:
                if coffre.Expired_Time and coffre.Expired_Time < datetime.now():
                    continue
                
                vaults_list.append(
                    {
                        "uuidCoffre": coffre.uuidCoffre,
                        "urlsite": coffre.urlsite,
                        "sitename" : coffre.sitename,
                        "urllogo": coffre.urllogo,
                    }
                )
            return jsonify(vaults_list)
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error getting vaults "+str(e)})

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

    def addVaultGroup(self,uuidUser, uuidGroup, uuidCoffre, isExpired):
        try:
            if not db.session.query(Groupe).filter(Groupe.uuidGroupe == uuidGroup, Groupe.uuidUserCreator == uuidUser).first():
                return jsonify({"status": "failed", "message": "Group not found"})
            if not db.session.query(Coffre).filter(Coffre.uuidCoffre == uuidCoffre).first():
                return jsonify({"status": "failed", "message": "Vault not found"})

            isExpired = datetime.now() + timedelta(days=1) if isExpired == 1 else None
            # if the vault is already shared to the group
            if not db.session.query(tablekeygroupe).filter(tablekeygroupe.uuidGroupe == uuidGroup, tablekeygroupe.uuidCoffre == uuidCoffre).first():
                partage = Partager(
                    uuidCoffre=uuidCoffre,
                    uuidGroupe=uuidGroup,
                    Created_Time=datetime.now(),
                    Expired_Time=isExpired
                )
                db.session.add(partage)
                db.session.commit()

                getSecretKey = db.session.query(tablekeyuser).filter(tablekeyuser.uuidUser == uuidUser, tablekeyuser.uuidCoffre == uuidCoffre).first()
                print(getSecretKey.keyvault)
                if not getSecretKey:
                    return jsonify({"status": "failed", "message": "Error adding vault to group"})

                keyvault =  getSecretKey.keyvault

                keygroupe = tablekeygroupe(
                    uuidGroupe=uuidGroup,
                    uuidCoffre=uuidCoffre,
                    keyvault=keyvault,
                    Created_Time = datetime.now(),
                    Expired_Time=isExpired
                )

                db.session.add(keygroupe)

                db.session.commit()

            return jsonify({"status": "success", "message": "Vault added to group"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error adding vault to group "+str(e)})

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

@app.route("/group/addvault", methods=['POST'])
@jwt_required()
def addVaultGroup():
    try:
        uuiduser = get_jwt_identity()
        paramettre = C.parametersissetPOST(['uuidGroup','uuidCoffre','isExpired'], request.json)
        if not paramettre:
            return jsonify({"status": "failed", "message": "Missing parameters"})

        uuidGroup = request.json.get('uuidGroup', None)
        uuidCoffre = request.json.get('uuidCoffre', None)
        isExpired = request.json.get('isExpired', 0)

        return group.addVaultGroup(uuiduser, uuidGroup, uuidCoffre,isExpired)
    except Exception as e:
        return jsonify({"status": "failed", "message": "Error adding vault to group "+str(e)})

@app.route("/group/listvault", methods=['GET'])
@jwt_required()
def listVaultGroup():
    try:
        uuiduser = get_jwt_identity()
        paramettre = C.parametersissetPOST(['uuidGroup'], request.json)
        if not paramettre:
            return jsonify({"status": "failed", "message": "Missing parameters"})

        uuidGroup = request.json.get('uuidGroup', None)

        return group.listVaultGroup(uuiduser, uuidGroup)
    except Exception as e:
        return jsonify({"status": "failed", "message": "Error getting vaults "+str(e)})