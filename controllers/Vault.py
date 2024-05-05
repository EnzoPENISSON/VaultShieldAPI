import json
import time
import uuid
from datetime import timedelta, datetime

from flask import jsonify, request
from ..models.dataclass import Utilisateur, Coffre, Classeur
from .. import app
from .. import db
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from .Chiffrement import Chiffrement
class Vault:

    def createVault(self,idcategorie, email, password, urlsite, urlogo, note,uuidkey,idUser):
            # convert uuidkey to bytes
            uuid_obj = uuid.UUID(uuidkey)

            # Convert UUID object to bytes
            uuid_bytes = uuid_obj.bytes

            coffrechiffre = Chiffrement(uuid_bytes)

            coffre = Coffre(
                idCategorie=idcategorie,
                email = email,
                password = password,
                urlsite = urlsite,
                urllogo = urlogo,
                note = note
            )
            coffrechiffre.ChiffrerVault(coffre)

            db.session.add(coffre)

            db.session.commit()

            ## add to classeur
            classeur = Classeur(
                idUser = idUser,
                idCoffre = coffre.idCoffre
            )
            return coffrechiffre.key

    def getVault(self, idCoffre):
        coffre = db.session.query(Coffre).filter(Coffre.idCoffre == idCoffre).first()
        if coffre:
            return json.dumps(
                {
                    "status": "success",
                    "message": "Vault found",
                    "email": coffre.email,
                    "password": coffre.password,
                    "urlsite": coffre.urlsite,
                    "urllogo": coffre.urllogo,
                    "note": coffre.note
                }
            )
        else:
            return json.dumps({"status": "failed", "message": "Vault not found"})



@app.route("/vault/add", methods=['POST'])
@jwt_required()
def createVault():
    data = request.get_json()
    idUser = get_jwt_identity()
    idcategorie = data['idcategorie']
    email = data['email']
    password = data['password']
    urlsite = data['urlsite']
    urllogo = data['urllogo']
    note = data['note']
    uuidkey = data['uuidkey']
    vault = Vault()
    key = vault.createVault(idcategorie, email, password, urlsite, urllogo, note,uuidkey,idUser)
    # convert the key to string
    key = key.decode()
    return jsonify({"status": "success", "message": "Vault created", "secretKey": key}), 201


@app.route("/vault/getall", methods=['GET'])
@jwt_required()
def getVaults():
    idUser = get_jwt_identity()
    coffres = []
    coffres_list = []
    for coffre in coffres:
        coffres_list.append(
            {
                "idCoffre": coffre.idCoffre,
                "email": coffre.email,
                "password": coffre.password,
                "urlsite": coffre.urlsite,
                "urllogo": coffre.urllogo,
                "note": coffre.note
            }
        )

    return json.dumps(coffres_list)