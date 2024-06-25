# coding: utf-8
from sqlalchemy.dialects.mssql import TINYINT

from .. import db

class Categorie(db.Model):
    __tablename__ = 'categorie'
    __table_args__ = {'extend_existing': True}

    uuidCategorie =  db.Column(db.String(100), primary_key=True)
    libCategorie =  db.Column(db.String(255), nullable=False)

class Groupe(db.Model):
    __tablename__ = 'groupe'
    __table_args__ = {'extend_existing': True}

    uuidGroupe =  db.Column(db.String(100), primary_key=True)
    uuidUserCreator  =  db.Column(db.ForeignKey('utilisateurs.uuidUser'), nullable=False,primary_key=True, index=True)
    Nom =  db.Column(db.String(50), nullable=False)

    Utilisateurs = db.relationship('utilisateurs')

class Partager(db.Model):
    __tablename__ = 'partager'
    __table_args__ = {'extend_existing': True}

    uuidGroupe = db.Column(db.ForeignKey('groupe.uuidGroupe'), primary_key=True, nullable=False, index=True)
    uuidCoffre = db.Column(db.ForeignKey('coffre.uuidCoffre'), primary_key=True, nullable=False, index=True)
    Created_Time = db.Column(db.DateTime, nullable=False, server_default=db.text("current_timestamp()"))
    Expired_Time = db.Column(db.DateTime, nullable=True)

    Groupe = db.relationship('groupe')
    Coffre = db.relationship('coffre')

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    __table_args__ = {'extend_existing': True}

    # idUser type UUID
    uuidUser = db.Column(db.String(100),primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    isAdmin = db.Column(TINYINT, nullable=False, server_default=db.text("0"))
    token = db.Column(db.String(512))
    last_co = db.Column(db.DateTime)
    OTP_code = db.Column(db.String(8), nullable=True)
    OTP_expired = db.Column(db.DateTime, nullable=True)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)


class Appartenir(db.Model):
    __tablename__ = 'appartenir'
    __table_args__ = {'extend_existing': True}

    uuidUser = db.Column(db.ForeignKey('utilisateurs.uuidUser'), primary_key=True, nullable=True, index=True)
    uuidCategorie = db.Column(db.ForeignKey('categorie.uuidCategorie'), primary_key=True, nullable=True, index=True)

    Categorie = db.relationship('categorie')
    Utilisateurs = db.relationship('utilisateurs')

    def __str__(self):
        return "idUser: "+str(self.uuidUser)+" idCategorie: "+str(self.uuidCategorie)

class Coffre(db.Model):
    __tablename__ = 'coffre'
    __table_args__ = {'extend_existing': True}

    uuidCoffre = db.Column(db.String(100), primary_key=True)
    uuidCategorie = db.Column(db.ForeignKey('Categorie.uuidCategorie'), index=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(512), nullable=False)
    sitename = db.Column(db.String(100), nullable=False)
    urlsite = db.Column(db.String(512), nullable=False)
    urllogo = db.Column(db.String(512), nullable=False)
    note = db.Column(db.String(512), nullable=False)

    Categorie = db.relationship('Categorie')

class Classeur(db.Model):
    __tablename__ = 'classeur'
    __table_args__ = {'extend_existing': True}

    uuidUser = db.Column(db.ForeignKey('utilisateurs.uuidUser'), primary_key=True, nullable=False)
    uuidCoffre = db.Column(db.ForeignKey('coffre.uuidCoffre'), primary_key=True, nullable=False, index=True)

    Coffre = db.relationship('coffre')
    Utilisateurs = db.relationship('utilisateurs')

    def __str__(self):
        return "idUser: "+str(self.uuidUser)+" idCoffre: "+str(self.uuidCoffre)

class sharegroupe_users(db.Model):
    __tablename__ = 'sharegroupe_users'
    __table_args__ = {'extend_existing': True}

    uuidGroupe = db.Column(db.ForeignKey('groupe.uuidGroupe'), primary_key=True, nullable=False, index=True)
    uuidUser = db.Column(db.ForeignKey('utilisateurs.uuidUser'), primary_key=True, nullable=False, index=True)
    Shared_Time = db.Column(db.DateTime, nullable=False, server_default=db.text("current_timestamp()"))
    Expired_Time = db.Column(db.DateTime, nullable=True)

    Groupe = db.relationship('groupe')
    Utilisateurs = db.relationship('utilisateurs')

    def __str__(self):
        return "idUser: "+str(self.idUser)+" idGroupe: "+str(self.idGroupe)



class tablekeyuser(db.Model):
    __bind_key__ = 'keyuser'
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'tablekeyuser'

    uuidUser = db.Column(db.String(100), primary_key=True)
    uuidCoffre = db.Column(db.String(100), primary_key=True)
    keyvault = db.Column(db.String(100), nullable=False)


class tablekeygroupe(db.Model):
    __bind_key__ = 'keyuser'
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'tablekeygroupe'

    uuidGroupe = db.Column(db.String(100), primary_key=True)
    uuidCoffre = db.Column(db.String(100), primary_key=True)
    keyvault = db.Column(db.String(100), nullable=False)
    Created_Time = db.Column(db.DateTime, nullable=False, server_default=db.text("current_timestamp()"))
    Expired_Time = db.Column(db.DateTime, nullable=True)

