from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_jwt_extended import JWTManager

app = Flask(__name__)

#server = "10.193.190.100"
server = "127.0.0.1"
database = "bddvaultshield"
username = "vaultuserAPI"
password = "UserVaultAPI*53"

# générer la chaine utilisée pour accéder ä la base et
param_bdd = "mysql+pymysql://"+username+":"+password+"@"+server+"/"+database
#print(param_bdd)
app.config['SQLALCHEMY_DATABASE_URI'] = param_bdd
# désactiver car gourmand en ressources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# créer une instance de Ia base de données

# Secret key for signing JWTs
app.config['JWT_SECRET_KEY'] = 'yhRHXnDfn%WozCcZziLNP#5wVwUK#5c46SZ7ZSxk'  # Change this to your own secret key
# add time expiration for the token
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900  # 15 minutes
# 7 hours
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 25200  # 7 hours

jwt = JWTManager(app)
db = SQLAlchemy(app)

# check if the connection is successfully established or not
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print('\n\nConnection successful !')
    except Exception as e:
        print('\n\nConnection failed ! ERROR : ', e)

from .controllers.Authcontrollers import *

@app.route("/")
def root():
    return "VaultShield"
