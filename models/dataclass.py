# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Table, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Categorie(Base):
    __tablename__ = 'Categorie'

    uuidCategorie = Column(String(100), primary_key=True)
    libCategorie = Column(String(255), nullable=False)

class Groupe(Base):
    __tablename__ = 'Groupe'

    uuidGroupe = Column(String(100), primary_key=True)
    uuidUserCreator  = Column(ForeignKey('Utilisateurs.uuidUser'), nullable=False,primary_key=True, index=True)
    Nom = Column(String(50), nullable=False)

    Utilisateurs = relationship('Utilisateur')

class Partager(Base):
    __tablename__ = 'Partager'

    uuidGroupe = Column(ForeignKey('Groupe.uuidGroupe'), primary_key=True, nullable=False, index=True)
    uuidCoffre = Column(ForeignKey('Coffre.uuidCoffre'), primary_key=True, nullable=False, index=True)
    Created_Time = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    Expired_Time = Column(DateTime, nullable=True)

    Groupe = relationship('Groupe')
    Coffre = relationship('Coffre')

class Utilisateur(Base):
    __tablename__ = 'Utilisateurs'

    # idUser type UUID
    uuidUser = Column(String(100),primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(512), nullable=False)
    isAdmin = Column(TINYINT(1), nullable=False, server_default=text("0"))
    token = Column(String(512))
    last_co = Column(DateTime)
    OTP_code = Column(String(8), nullable=True)
    OTP_expired = Column(DateTime, nullable=True)
    reset_token = Column(String(255), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)


class Appartenir(Base):
    __tablename__ = 'Appartenir'

    uuidUser = Column(ForeignKey('Utilisateurs.uuidUser'), primary_key=True, nullable=True, index=True)
    uuidCategorie = Column(ForeignKey('Categorie.uuidCategorie'), primary_key=True, nullable=True, index=True)

    Categorie = relationship('Categorie')
    Utilisateurs = relationship('Utilisateur')

    def __str__(self):
        return "idUser: "+str(self.idUser)+" idCategorie: "+str(self.idCategorie)

class Coffre(Base):
    __tablename__ = 'Coffre'

    uuidCoffre = Column(String(100), primary_key=True)
    uuidCategorie = Column(ForeignKey('Categorie.uuidCategorie'), index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(512), nullable=False)
    sitename = Column(String(100), nullable=False)
    urlsite = Column(String(512), nullable=False)
    urllogo = Column(String(512), nullable=False)
    note = Column(String(512), nullable=False)

    Categorie = relationship('Categorie')

class Classeur(Base):
    __tablename__ = 'Classeur'

    uuidUser = Column(ForeignKey('Utilisateurs.uuidUser'), primary_key=True, nullable=False)
    uuidCoffre = Column(ForeignKey('Coffre.uuidCoffre'), primary_key=True, nullable=False, index=True)

    Coffre = relationship('Coffre')
    Utilisateurs = relationship('Utilisateur')

    def __str__(self):
        return "idUser: "+str(self.idUser)+" idCoffre: "+str(self.idCoffre)

class sharegroupe_users(Base):
    __tablename__ = 'sharegroupe_users'

    uuidGroupe = Column(ForeignKey('Groupe.uuidGroupe'), primary_key=True, nullable=False, index=True)
    uuidUser = Column(ForeignKey('Utilisateurs.uuidUser'), primary_key=True, nullable=False, index=True)
    Shared_Time = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    Expired_Time = Column(DateTime, nullable=True)

    Groupe = relationship('Groupe')
    Utilisateurs = relationship('Utilisateur')

    def __str__(self):
        return "idUser: "+str(self.idUser)+" idGroupe: "+str(self.idGroupe)
