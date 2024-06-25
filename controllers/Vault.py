import json
import uuid
from .Controller import ControllerClass as C
from flask import jsonify, request
from ..models.dataclass import Utilisateur, Coffre, Classeur, tablekeyuser
from .utilitytool import UtilityTool
from .CategorieController import CategoryController
from .. import app
from .. import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from .Chiffrement import Chiffrement
class Vault:
    tool = UtilityTool()
    def createVault(self, data):
        try:
            # convert uuidkey to bytes
            uuid1, uuid2 = self.tool.split_and_convert_two_uuids(str(data["uuidUser"]))

            # Convert UUID object to bytes
            uuid_bytes = uuid1.bytes + uuid2.bytes
            coffrechiffre = Chiffrement(uuid_bytes)

            categorie = data.get("uuidcategorie", None)

            if categorie:
                categories = CategoryController()
                listcategoriesuser = categories.getCategoriesIdentifiant(data["uuidUser"])

                if categorie not in listcategoriesuser:
                    return jsonify({"status": "failed", "message": "Category not found"})

            coffre = Coffre(
                uuidCategorie=categorie,
                uuidCoffre=self.tool.longUUIDGenerator(),
                username=data.get("username", ""),
                email=data.get("email", ""),
                password=data.get("password", ""),
                sitename=data.get("sitename", ""),
                urlsite=data.get("urlsite", ""),
                urllogo=data.get("urllogo", ""),
                note=data.get("note", "")
            )

            coffrechiffre.ChiffrerVault(coffre)

            db.session.add(coffre)

            db.session.commit()
            identifiantUtilistaure = db.session.query(Utilisateur).filter(
                Utilisateur.uuidUser == data["uuidUser"]).first()

            ## add to classeur
            classeur = Classeur(
                uuidUser=identifiantUtilistaure.uuidUser,
                uuidCoffre=coffre.uuidCoffre
            )

            db.session.add(classeur)

            db.session.commit()

            # save key in keyvault
            clef = tablekeyuser(
                uuidUser=data["uuidUser"],
                uuidCoffre=coffre.uuidCoffre,
                keyvault=coffrechiffre.key
            )
            print(clef)
            db.session.add(clef)

            db.session.commit()
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error creating vault "+str(e)})

    def getSecretKey(self, uuidUser, uuidCoffre):
        try:
            clef = db.session.query(tablekeyuser).filter(tablekeyuser.uuidUser == uuidUser).filter(
                tablekeyuser.uuidCoffre == uuidCoffre).first()

            if not clef:
                return None

            return clef.keyvault
        except Exception as e:
            return None

    def getVaults(self, uuidUser):

        try :
            coffres = db.session.query(Coffre).join(Classeur).filter(Classeur.uuidUser == uuidUser).all()
            coffres_list = []
            for coffre in coffres:
                coffres_list.append(
                    {
                        "uuidCoffre": coffre.uuidCoffre,
                        "urlsite": coffre.urlsite,
                        "sitename": coffre.sitename,
                        "urllogo": coffre.urllogo,
                    }
                )

            return coffres_list
        except Exception as e:
            return []

    def getVault(self, uuidUser, uuidCoffre):
        try:
            coffre = db.session.query(Coffre).join(Classeur).filter(Classeur.uuidUser == uuidUser).filter(
                Coffre.uuidCoffre == uuidCoffre).first()

            return coffre
        except Exception as e:
            return None

    def updateVault(self, data):
        try:
            uuidcoffre = data["uuidCoffre"]
            iduser = data["uuidUser"]

            coffre = db.session.query(Coffre).join(Classeur).filter(Classeur.uuidUser == iduser).filter(
                Coffre.uuidCoffre == uuidcoffre).first()

            if not coffre:
                return None

            # parcourir les données
            for key, value in data.items():
                if key == "username":
                    coffre.username = value
                if key == "email":
                    coffre.email = value
                elif key == "password":
                    coffre.password = value
                elif key == "sitename":
                    coffre.sitename = value
                elif key == "urlsite":
                    coffre.urlsite = value
                elif key == "urllogo":
                    coffre.urllogo = value
                elif key == "note":
                    coffre.note = value

            uuid1, uuid2 = self.tool.split_and_convert_two_uuids(str(iduser))

            # Convert UUID object to bytes
            uuid_bytes = uuid1.bytes + uuid2.bytes

            coffrechiffre = Chiffrement(uuid_bytes)

            coffrechiffre.updateVault(coffre, data["secretkey"])

            db.session.commit()

            return coffre
        except Exception as e:
            return None

    def deleteCoffre(self, uuidUser, uuidCoffre):
        try:
            classeur = db.session.query(Classeur).filter(Classeur.uuidUser == uuidUser).filter(
                Classeur.uuidCoffre == uuidCoffre).first()

            if not classeur:
                return None

            db.session.delete(classeur)

            db.session.commit()

            coffre = db.session.query(Coffre).filter(Coffre.uuidCoffre == uuidCoffre).first()

            if not coffre:
                return None

            db.session.delete(coffre)

            db.session.commit()

            return coffre
        except Exception as e:
            return None

    def AssocierCategorie(self, uuidUser, uuidCategorie, uuidCoffre):
        try:
            categories = CategoryController()

            listcategoriesuser = categories.getCategoriesIdentifiant(uuidUser)

            if uuidCategorie not in listcategoriesuser:
                return jsonify({"status": "failed", "message": "Category not found"})

            coffre = db.session.query(Coffre).filter(Coffre.uuidCoffre == uuidCoffre).first()

            if not coffre:
                return jsonify({"status": "failed", "message": "Coffre not found"})

            coffre.uuidCategorie = uuidCategorie

            db.session.commit()

            return jsonify({"status": "success", "message": "Category added"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error adding category "+str(e)})

    def removeCategorieFromVault(self, uuidUser, uuidCoffre):
        try:
            # recupérer le coffre et faire une jointure avec l'utilisateur
            coffre = db.session.query(Coffre).join(Classeur).filter(Classeur.uuidUser == uuidUser).filter(Coffre.uuidCoffre == uuidCoffre).first()

            if not coffre:
                return jsonify({"status": "failed", "message": "Vault not found"})

            coffre.uuidCategorie = None

            db.session.commit()

            return jsonify({"status": "success", "message": "Category removed"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error removing category "+str(e)})

@app.route("/vault/add", methods=['POST'])
@jwt_required()
def createVault():
    data = request.get_json()
    uuidUser = get_jwt_identity()
    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    # Update the dictionary with the new key-value pair
    dictdata.update({"uuidUser": uuidUser})

    vault = Vault()
    vault.createVault(dictdata)
    return jsonify({"status": "success", "message": "Vault created"}), 201


@app.route("/vault/getall", methods=['GET'])
@jwt_required()
def getVaults():
    uuidUser = get_jwt_identity()
    vault = Vault()
    coffres = vault.getVaults(uuidUser)

    return jsonify(coffres)


@app.route("/vault/get", methods=['POST'])
@jwt_required()
def getVault():
    paramettre = C.parametersissetPOST(['uuidCoffre', 'secretkey'], request.json)

    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})


    data = request.get_json()

    uuidUser = get_jwt_identity()
    uuidCoffre = data["uuidCoffre"]

    secretkey = data["secretkey"]

    vault = Vault()
    coffre = vault.getVault(uuidUser, uuidCoffre)

    if not coffre:
        return jsonify({"status": "failed", "message": "Vault not found"})
    tool = UtilityTool()
    uuid1, uuid2 = tool.split_and_convert_two_uuids(str(uuidUser))

    uuidkey = uuid1.bytes + uuid2.bytes

    coffrechiffre = Chiffrement(uuidkey)

    return jsonify(
        {
            "uuidCoffre": coffre.uuidCoffre,
            "uuidCategorie": coffre.uuidCategorie,
            "username": coffrechiffre.decrypt_password(coffre.username, secretkey.encode(), uuidkey),
            "email": coffrechiffre.decrypt_password(coffre.email, secretkey.encode(), uuidkey),
            "password": coffrechiffre.decrypt_password(coffre.password, secretkey.encode(), uuidkey),
            "sitename": coffre.sitename,
            "urlsite": coffre.urlsite,
            "urllogo": coffre.urllogo,
            "note": coffrechiffre.decrypt_password(coffre.note, secretkey.encode(), uuidkey)
        }
    )

@app.route("/vault/update", methods=['PUT'])
@jwt_required()
def updateVault():
    data = request.get_json()
    uuidUser = get_jwt_identity()


    outils = UtilityTool()

    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    dictdata.update({"uuidUser": uuidUser})

    vault = Vault()
    coffre = vault.updateVault(dictdata)

    if not coffre:
        return jsonify({"status": "failed", "message": "Vault not found"})

    return jsonify({"status": "success", "message": "Vault updated"}), 201


@app.route("/vault/delete", methods=['POST'])
@jwt_required()
def deleteVault():
    data = request.get_json()
    uuiduser = get_jwt_identity()

    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    vault = Vault()
    coffre = vault.deleteCoffre(uuiduser, dictdata["uuidCoffre"])

    if not coffre:
        return jsonify({"status": "failed", "message": "Vault not found"})

    return jsonify({"status": "success", "message": "Vault deleted"}), 201


@app.route("/vault/category/associer", methods=['POST'])
@jwt_required()
def associerCategorie():
    data = request.get_json()
    uuidUser = get_jwt_identity()

    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    vault = Vault()
    res = vault.AssocierCategorie(uuidUser, dictdata["uuidCategorie"], dictdata["uuidCoffre"])

    return res

@app.route("/vault/category/remove", methods=['PUT'])
@jwt_required()
def removeCategorieFromVault():
    data = request.get_json()
    uuidUser = get_jwt_identity()

    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    vault = Vault()
    res = vault.removeCategorieFromVault(uuidUser,dictdata["uuidCoffre"])

    return res


@app.route("/vault/secretkey", methods=['POST'])
@jwt_required()
def getSecretKey():
    data = request.get_json()
    uuidUser = get_jwt_identity()

    vault = Vault()
    key = vault.getSecretKey(uuidUser, data["uuidCoffre"])

    if not key:
        return jsonify({"status": "failed", "message": "Key not found"})

    return jsonify({"status": "success", "key": key})