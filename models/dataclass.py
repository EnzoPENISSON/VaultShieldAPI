# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Table, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Categorie(Base):
    __tablename__ = 'Categorie'

    idCategorie = Column(INTEGER(11), primary_key=True)
    libCategorie = Column(String(255), nullable=False)

class Groupe(Base):
    __tablename__ = 'Groupe'

    idGroupe = Column(INTEGER(11), primary_key=True)
    Nom = Column(INTEGER(11), nullable=False)


class Utilisateur(Base):
    __tablename__ = 'Utilisateurs'

    # idUser type UUID
    idUser = Column(INTEGER(11), primary_key=True)
    uuidUser = Column(String(40))
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(512), nullable=False)
    isAdmin = Column(TINYINT(1), nullable=False, server_default=text("0"))
    token = Column(String(512))
    last_co = Column(DateTime)


class Appartenir(Base):
    __tablename__ = 'Appartenir'

    idUser = Column(ForeignKey('Utilisateurs.idUser'), primary_key=True, nullable=True, index=True)
    idCategorie = Column(ForeignKey('Categorie.idCategorie'), primary_key=True, nullable=True, index=True)

    Categorie = relationship('Categorie')
    Utilisateurs = relationship('Utilisateur')

    def __str__(self):
        return "idUser: "+str(self.idUser)+" idCategorie: "+str(self.idCategorie)

class Coffre(Base):
    __tablename__ = 'Coffre'

    idCoffre = Column(INTEGER(11), primary_key=True)
    idCategorie = Column(ForeignKey('Categorie.idCategorie'), index=True)
    uuidCoffre = Column(String(100))
    email = Column(String(255), nullable=False)
    password = Column(String(512), nullable=False)
    sitename = Column(String(100), nullable=False)
    urlsite = Column(String(512), nullable=False)
    urllogo = Column(String(512), nullable=False)
    note = Column(String(512), nullable=False)

class Classeur(Base):
    __tablename__ = 'Classeur'

    idUser = Column(ForeignKey('Utilisateurs.idUser'), primary_key=True, nullable=False)
    idCoffre = Column(ForeignKey('Coffre.idCoffre'), primary_key=True, nullable=False, index=True)

    Coffre = relationship('Coffre')
    Utilisateurs = relationship('Utilisateur')

    def __str__(self):
        return "idUser: "+str(self.idUser)+" idCoffre: "+str(self.idCoffre)

