from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)


# Enable CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = 'lemeilleurcoffredemotdepassedumondevoirmemedelunivers'
# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'noreply.vaultshield@gmail.com'
app.config['MAIL_PASSWORD'] = 'hsejnhohsibdecqn'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

#server = "127.0.0.1"
server = "127.0.0.1:3310"
database = "bddvaultshield"
database2 = "bddkeyvault"
username = "vaultuserAPI"
password = "UserVaultAPI*53"

# générer la chaine utilisée pour accéder ä la base et
param_bdd = "mysql+pymysql://"+username+":"+password+"@"+server+"/"+database
param_bdd2 = "mysql+pymysql://"+username+":"+password+"@"+server+"/"+database2

app.config['SQLALCHEMY_DATABASE_URI'] = param_bdd
app.config['SQLALCHEMY_BINDS'] = {
    'keyuser': param_bdd2
}

# désactiver car gourmand en ressources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# créer une instance de Ia base de données

# Secret key for signing JWTs
app.config['JWT_SECRET_KEY'] = 'yhRHXnDfn%WozCcZziLNP#5wVwUK#5c46SZ7ZSxk'  # Change this to your own secret key
# add time expiration for the token
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 # 1 hour

jwt = JWTManager(app)

db = SQLAlchemy(app)

# check if the connection is successfully established or not
with app.app_context():
    try:
        db.create_all()
        db.session.execute(text('SELECT 1'))
        print('\n\nConnection successful !')
    except Exception as e:
        print('\n\nConnection failed ! ERROR : ', e)

from .controllers.Authcontrollers import *
from .controllers.Vault import *
from .controllers.UserController import *
from .controllers.CategorieController import *
from .controllers.GroupeController import *
from .controllers.AdminControllers import *


@app.route("/")
def root():
    return "VaultShield"
