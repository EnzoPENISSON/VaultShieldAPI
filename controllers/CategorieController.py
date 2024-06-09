from .Controller import ControllerClass as C

from flask import jsonify, request
from ..models.dataclass import Categorie, Appartenir, Coffre, Classeur
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

    def getCategoriesIdentifiant(self, idUser):
        try:
            categories = db.session.query(Categorie).join(Appartenir).filter(Appartenir.idUser == idUser).all()
            categories_list = []
            for categorie in categories:
                categories_list.append(
                    categorie.idCategorie
                )
            return categories_list
        except Exception as e:
            print("error getting categories "+str(e))
            return []
    def getCategories(self, idUser):
        try:
            categories = db.session.query(Categorie).join(Appartenir).filter(Appartenir.idUser == idUser).all()
            categories_list = []
            for categorie in categories:
                categories_list.append(
                    {
                        "idCategorie": categorie.idCategorie,
                        "libCategorie": categorie.libCategorie
                    }
                )
            return jsonify({"status": "success", "categories": categories_list})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error getting categories "+str(e)})

    def getListVaultsWithCategory(self, idUser, idCategorie):
        try:
            from .Vault import Vault
            vaults = Vault()
            vaults = vaults.getVaults(idUser)
            return vaults
        except Exception as e:
            return "error getting vaults with category "+str(e)

    def removeCategory(self, emailuser, idUser, idCategorie):
        try:
            listV = self.getListVaultsWithCategory(emailuser, idCategorie)

            if listV:
                for v in listV:
                    # replace idCategorie by null
                    coffre = db.session.query(Coffre).filter(Coffre.uuidCoffre == v["uuidCoffre"]).first()
                    coffre.idCategorie = None
                    db.session.commit()


            appartenir = db.session.query(Appartenir).filter(Appartenir.idCategorie == idCategorie).filter(Appartenir.idUser == idUser).first()
            if appartenir:
                 db.session.delete(appartenir)
                 db.session.commit()
                 return jsonify({"status": "success", "message": "Category removed"})
            else:
                 return jsonify({"status": "failed", "message": "Category not found"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error removing category "+str(e)})

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

@app.route("/category/get", methods=['GET'])
@jwt_required()
def getCategories():
    useremail = get_jwt_identity()

    user = Tools()
    res = user.userExist(useremail, request.json)
    if res:
        return res

    userid = user.getUserId(useremail)

    res = Category.getCategories(userid)
    return res

@app.route("/category/remove", methods=['DELETE'])
@jwt_required()
def removeCategory():
    paramettre = C.parametersissetPOST(['idCategorie'], request.json)
    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})
    idCategorie = request.json.get('idCategorie', None)
    useremail = get_jwt_identity()

    user = Tools()
    res = user.userExist(useremail, request.json)
    if res:
        return res

    userid = user.getUserId(useremail)

    if idCategorie:
        res = Category.removeCategory(useremail,userid, idCategorie)
        return res
    else:
        return jsonify({"status": "failed", "message": "Invalid category id"})