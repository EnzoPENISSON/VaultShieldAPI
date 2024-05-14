import json
import uuid
from .Controller import ControllerClass as C
from flask import jsonify, request
from ..models.dataclass import Utilisateur, Coffre, Classeur
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
    paramettre = C.parametersissetPOST(['uuidCoffre'], request.json)
    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})


    data = request.get_json()

    idUser = get_jwt_identity()
    uuidCoffre = data["uuidCoffre"]

    vault = Vault()
    coffre = vault.getVault(idUser, uuidCoffre)

    return jsonify(
        {
            "uuidCoffre": coffre.uuidCoffre,
            "email": coffre.email,
            "password": coffre.password,
            "sitename": coffre.sitename,
            "urlsite": coffre.urlsite,
            "urllogo": coffre.urllogo,
            "note": coffre.note
        }
    )