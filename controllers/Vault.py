import json
import uuid
from .Controller import ControllerClass as C
from flask import jsonify, request
from ..models.dataclass import Utilisateur, Coffre, Classeur
from .tools import *
from .CategorieController import CategoryController
from .. import app
from .. import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from .Chiffrement import Chiffrement
class Vault:

    def createVault(self, data):
            # convert uuidkey to bytes
            uuid_obj = uuid.UUID(data["uuidkey"])

            # Convert UUID object to bytes
            uuid_bytes = uuid_obj.bytes

            coffrechiffre = Chiffrement(uuid_bytes)

            coffre = Coffre(
                idCategorie=data["idcategorie"],
                uuidCoffre = uuid.uuid5(uuid.NAMESPACE_DNS, data["email"]).hex,
                username = data["username"],
                email = data["email"],
                password = data["password"],
                sitename = data["sitename"],
                urlsite = data["urlsite"],
                urllogo = data["urllogo"],
                note = data["note"]
            )
            coffrechiffre.ChiffrerVault(coffre)

            db.session.add(coffre)

            db.session.commit()

            identifiantUtilistaure = db.session.query(Utilisateur).filter(Utilisateur.email == data["idUser"]).first()

            ## add to classeur
            classeur = Classeur(
                idUser = identifiantUtilistaure.idUser,
                idCoffre = coffre.idCoffre
            )

            print("Classeur:",classeur.__str__())

            db.session.add(classeur)

            db.session.commit()

            return coffrechiffre.key

    def getVaults(self, idUser):
        identifiantUtilistaure = db.session.query(Utilisateur).filter(Utilisateur.email == idUser).first()

        coffres = db.session.query(Coffre).join(Classeur).filter(Classeur.idUser == identifiantUtilistaure.idUser).all()
        coffres_list = []
        for coffre in coffres:
            coffres_list.append(
                {
                    "uuidCoffre": coffre.uuidCoffre,
                    "urlsite": coffre.urlsite,
                    "urllogo": coffre.urllogo,
                }
            )

        return coffres_list

    def getVault(self, idUser, uuidCoffre):
        identifiantUtilistaure = db.session.query(Utilisateur).filter(Utilisateur.email == idUser).first()

        coffre = db.session.query(Coffre).join(Classeur).filter(Classeur.idUser == identifiantUtilistaure.idUser).filter(Coffre.uuidCoffre == uuidCoffre).first()

        return coffre

    def updateVault(self, data,uuidCoffre,iduser):
        identifiantUtilistaure = db.session.query(Utilisateur).filter(Utilisateur.email == iduser).first()

        coffre = db.session.query(Coffre).join(Classeur).filter(Classeur.idUser == identifiantUtilistaure.idUser).filter(Coffre.uuidCoffre == uuidCoffre).first()

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

        uuid_obj = uuid.UUID(data["userUUid"])

        # Convert UUID object to bytes
        uuid_bytes = uuid_obj.bytes

        coffrechiffre = Chiffrement(uuid_bytes)

        coffrechiffre.updateVault(coffre,data["secretkey"])

        db.session.commit()

        return coffre

    def deleteCoffre(self, idUser, uuidCoffre):
        identifiantUtilistaure = db.session.query(Utilisateur).filter(Utilisateur.email == idUser).first()

        coffre = db.session.query(Coffre).join(Classeur).filter(Classeur.idUser == identifiantUtilistaure.idUser).filter(Coffre.uuidCoffre == uuidCoffre).first()

        if not coffre:
            return None

        db.session.delete(coffre)

        db.session.commit()

        return coffre

    def AssocierCategorie(self, idUser, idCategorie, idCoffre):
        try:
            categories = CategoryController()

            listcategoriesuser = categories.getCategoriesIdentifiant(idUser)

            if idCategorie not in listcategoriesuser:
                return jsonify({"status": "failed", "message": "Category not found"})

            coffre = db.session.query(Coffre).filter(Coffre.uuidCoffre == idCoffre).first()

            if not coffre:
                return jsonify({"status": "failed", "message": "Vault not found"})

            coffre.idCategorie = idCategorie

            db.session.commit()

            return jsonify({"status": "success", "message": "Category added"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error adding category "+str(e)})

    def removeCategorieFromVault(self, idUser, idCoffre):
        try:
            # recupérer le coffre et faire une jointure avec l'utilisateur
            coffre = db.session.query(Coffre).join(Classeur).filter(Classeur.idUser == idUser).filter(Coffre.uuidCoffre == idCoffre).first()

            if not coffre:
                return jsonify({"status": "failed", "message": "Vault not found"})

            coffre.idCategorie = None

            db.session.commit()

            return jsonify({"status": "success", "message": "Category removed"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error removing category "+str(e)})

@app.route("/vault/add", methods=['POST'])
@jwt_required()
def createVault():
    data = request.get_json()
    idUser = get_jwt_identity()
    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    # Update the dictionary with the new key-value pair
    dictdata.update({"idUser": idUser})

    print("Data:",dictdata)


    vault = Vault()
    key = vault.createVault(dictdata)
    # convert the key to string
    key = key.decode()
    return jsonify({"status": "success", "message": "Vault created", "secretKey": key}), 201


@app.route("/vault/getall", methods=['GET'])
@jwt_required()
def getVaults():
    idUser = get_jwt_identity()
    vault = Vault()
    coffres = vault.getVaults(idUser)

    return jsonify(coffres)


@app.route("/vault/get", methods=['POST'])
@jwt_required()
def getVault():
    paramettre = C.parametersissetPOST(['uuidCoffre', 'secretkey', 'userUUid'], request.json)

    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})


    data = request.get_json()

    idUser = get_jwt_identity()
    uuidCoffre = data["uuidCoffre"]

    secretkey = data["secretkey"]

    userUUid = data["userUUid"]

    vault = Vault()
    coffre = vault.getVault(idUser, uuidCoffre)

    if not coffre:
        return jsonify({"status": "failed", "message": "Vault not found"})

    coffrechiffre = Chiffrement(uuid.UUID(userUUid).bytes)

    return jsonify(
        {
            "uuidCoffre": coffre.uuidCoffre,
            "username": coffrechiffre.decrypt_password(coffre.username, secretkey.encode(), uuid.UUID(userUUid).bytes),
            "email": coffrechiffre.decrypt_password(coffre.email, secretkey.encode(), uuid.UUID(userUUid).bytes),
            "password": coffrechiffre.decrypt_password(coffre.password, secretkey.encode(), uuid.UUID(userUUid).bytes),
            "sitename": coffre.sitename,
            "urlsite": coffre.urlsite,
            "urllogo": coffre.urllogo,
            "note": coffrechiffre.decrypt_password(coffre.note, secretkey.encode(), uuid.UUID(userUUid).bytes)
        }
    )

@app.route("/vault/update", methods=['PUT'])
@jwt_required()
def updateVault():
    data = request.get_json()
    idUser = get_jwt_identity()


    outils = Tools()
    user = outils.userExist(idUser, data)
    if user:
        return user

    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    # Update the dictionary with the new key-value pair
    userId = outils.getUserUUID(idUser)

    dictdata.update({"idUser": userId})

    vault = Vault()
    coffre = vault.updateVault(dictdata, dictdata["uuidCoffre"], idUser)

    if not coffre:
        return jsonify({"status": "failed", "message": "Vault not found"})

    return jsonify({"status": "success", "message": "Vault updated"}), 201


@app.route("/vault/delete", methods=['DELETE'])
@jwt_required()
def deleteVault():
    data = request.get_json()
    idUser = get_jwt_identity()

    outils = Tools()
    user = outils.userExist(idUser, data)
    if user:
        return user

    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    # Update the dictionary with the new key-value pair
    userId = outils.getUserUUID(idUser)

    dictdata.update({"idUser": userId})

    vault = Vault()
    coffre = vault.deleteCoffre(idUser, dictdata["uuidCoffre"])

    if not coffre:
        return jsonify({"status": "failed", "message": "Vault not found"})

    return jsonify({"status": "success", "message": "Vault deleted"}), 201


@app.route("/vault/category/associer", methods=['POST'])
@jwt_required()
def associerCategorie():
    data = request.get_json()
    idUser = get_jwt_identity()

    outils = Tools()
    user = outils.userExist(idUser, data)
    if user:
        return user

    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    # Update the dictionary with the new key-value pair
    userId = outils.getUserId(idUser)

    dictdata.update({"idUser": userId})

    vault = Vault()
    res = vault.AssocierCategorie(dictdata["idUser"], dictdata["idCategorie"], dictdata["idCoffre"])

    return res

@app.route("/vault/category/remove", methods=['PUT'])
@jwt_required()
def removeCategorieFromVault():
    data = request.get_json()
    idUser = get_jwt_identity()

    outils = Tools()
    user = outils.userExist(idUser, data)
    if user:
        return user

    dictdata = json.dumps(data)

    # Convert the JSON string back to a Python dictionary
    dictdata = json.loads(dictdata)

    # Update the dictionary with the new key-value pair
    userId = outils.getUserId(idUser)

    dictdata.update({"idUser": userId})

    vault = Vault()
    res = vault.removeCategorieFromVault(dictdata["idUser"],dictdata["idCoffre"])

    return res