from .Controller import ControllerClass as C

from flask import jsonify, request
from ..models.dataclass import Categorie, Appartenir
from .tools import Tools
from .. import app
from .. import db
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
class CategoryController:

    def ajouterCategorie(self, idUser, nomCategorie):
        try:
            categorie = Categorie(libCategorie=nomCategorie)

            # si pas dans la base on ajoute
            if not db.session.query(Categorie).filter(Categorie.libCategorie == nomCategorie).first():
                db.session.add(categorie)
                db.session.commit()

            categorieid = db.session.query(Categorie).filter(Categorie.libCategorie == nomCategorie).first()

            if not db.session.query(Appartenir).filter(Appartenir.idCategorie == categorieid.idCategorie).filter(Appartenir.idUser == idUser).first():
                appartenir = Appartenir(idCategorie=categorieid.idCategorie, idUser=idUser)
                db.session.add(appartenir)
                db.session.commit()
            return jsonify({"status": "success", "message": "Category added"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error adding category "+str(e)})





Category = CategoryController()

@app.route("/category/add", methods=['POST'])
@jwt_required()
def addCategory():
    paramettre = C.parametersissetPOST(['nomCategorie'], request.json)
    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})
    nomCategorie = request.json.get('nomCategorie', None)
    useremail = get_jwt_identity()

    user = Tools()
    res = user.userExist(useremail, request.json)
    if res:
        return res

    userid = user.getUserId(useremail)

    if nomCategorie:
        res = Category.ajouterCategorie(userid, nomCategorie)
        return res
    else:
        return jsonify({"status": "failed", "message": "Invalid category name"})