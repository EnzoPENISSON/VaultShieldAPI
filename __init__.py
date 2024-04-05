from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

server = "10.193.190.100"
database = "bddvaultshield"
username = "vaultuserAPI"
password = "UserVaultAPI*53"
'mysql+pymysql://vaultuserAPI:UserVaultAPI*53@10.193.190.100/bddvaultshield'
# générer la chaine utilisée pour accéder ä la base et
param_bdd = "mysql+pymysql://"+username+":"+password+"@"+server+"/"+database
print(param_bdd)
app.config['SQLALCHEMY_DATABASE_URI'] = param_bdd
# désactiver car gourmand en ressources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# créer une instance de Ia base de données

db = SQLAlchemy(app)

# check if the connection is successfully established or not
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print('\n\nConnection successful !')
    except Exception as e:
        print('\n\nConnection failed ! ERROR : ', e)


@app.route("/")
def root():
    return "VaultShield"


app.run(port=8080, debug=True)