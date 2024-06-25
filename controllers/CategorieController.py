from .Controller import ControllerClass as C

from flask import jsonify, request
from ..models.dataclass import Categorie, Appartenir, Coffre, Classeur
from .utilitytool import UtilityTool
from .. import app
from .. import db
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt


class CategoryController:
    tool = UtilityTool()
    def ajouterCategorie(self, uuidUser, nomCategorie):
        try:
            categorie = Categorie(
                uuidCategorie=self.tool.longUUIDGenerator(),
                libCategorie=nomCategorie
            )

            # si pas dans la base on ajoute
            if not db.session.query(Categorie).filter(Categorie.libCategorie == nomCategorie).first():
                db.session.add(categorie)
                db.session.commit()

            categorieid = db.session.query(Categorie).filter(Categorie.libCategorie == nomCategorie).first()

            if not db.session.query(Appartenir).filter(Appartenir.uuidCategorie == categorieid.uuidCategorie).filter(Appartenir.uuidUser == uuidUser).first():
                appartenir = Appartenir(uuidCategorie=categorieid.uuidCategorie, uuidUser=uuidUser)
                db.session.add(appartenir)
                db.session.commit()
            return jsonify({"status": "success", "message": "Category added"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error adding category "+str(e)})

    def getCategoriesIdentifiant(self, uuidUser):
        try:
            categories = db.session.query(Categorie).join(Appartenir).filter(Appartenir.uuidUser == uuidUser).all()
            categories_list = []
            for categorie in categories:
                categories_list.append(
                    categorie.uuidCategorie
                )
            return categories_list
        except Exception as e:
            print("error getting categories "+str(e))
            return []
    def getCategories(self, uuidUser):
        try:
            categories = db.session.query(Categorie).join(Appartenir).filter(Appartenir.uuidUser == uuidUser).all()
            categories_list = []
            for categorie in categories:
                categories_list.append(
                    {
                        "idCategorie": categorie.uuidCategorie,
                        "libCategorie": categorie.libCategorie
                    }
                )
            return jsonify(categories_list)
        except Exception as e:
            return jsonify({"status": "failed", "message": "Error getting categories "+str(e)})

    def getListVaultsWithCategory(self, uuidUser):
        try:
            from .Vault import Vault
            vaults = Vault()
            vaults = vaults.getVaults(uuidUser)
            return vaults
        except Exception as e:
            return "error getting vaults with category "+str(e)

    def removeCategory(self, uuidUser, uuidCategorie):
        try:
            listV = self.getListVaultsWithCategory(uuidUser)

            if listV:
                for v in listV:
                    # replace idCategorie by null
                    coffre = db.session.query(Coffre).filter(Coffre.uuidCoffre == v["uuidCoffre"]).first()
                    coffre.uuidCategorie = None
                    db.session.commit()


            appartenir = db.session.query(Appartenir).filter(Appartenir.uuidCategorie == uuidCategorie).filter(Appartenir.uuidUser == uuidUser).first()
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
    uuidUser = get_jwt_identity()


    if nomCategorie:
        res = Category.ajouterCategorie(uuidUser, nomCategorie)
        return res
    else:
        return jsonify({"status": "failed", "message": "Invalid category name"})

@app.route("/category/get", methods=['GET'])
@jwt_required()
def getCategories():
    uuiduser = get_jwt_identity()

    return Category.getCategories(uuiduser)

@app.route("/category/remove", methods=['DELETE'])
@jwt_required()
def removeCategory():
    paramettre = C.parametersissetPOST(['uuidCategorie'], request.json)
    if not paramettre:
        return jsonify({"status": "failed", "message": "Missing parameters"})
    uuidCategorie = request.json.get('uuidCategorie', None)
    uuidUser = get_jwt_identity()

    if uuidCategorie:
        res = Category.removeCategory(uuidUser, uuidCategorie)
        return res
    else:
        return jsonify({"status": "failed", "message": "Invalid category id"})