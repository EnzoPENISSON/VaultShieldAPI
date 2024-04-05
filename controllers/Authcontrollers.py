from flask import jsonify,request

from .. import app
from .. import db
import bcrypt
from models import Utilisateur
class Authentification:

    def login(self,email,password):
        listUser = db.session.query(Utilisateur).filter(Utilisateur.email == email)

        for user in listUser:
            enc_pw = user.password.encode('utf-8')
            checkpassword = bcrypt.checkpw(enc_pw, bytes(password, 'utf-8'))
            if checkpassword == True:
                return jsonify(
                    user
                )

        return False


auth = Authentification()

@app.route("/auth/login", methods=['POST'])
def login():
    req_data = request.get_json(force=True)
    return auth.login(req_data['email'],req_data['password'])
