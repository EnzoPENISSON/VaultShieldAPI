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

    Utilisateurs = relationship('Utilisateur', secondary='Appartenir')


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


t_Appartenir = Table(
    'Appartenir', metadata,
    Column('idUser', ForeignKey('Utilisateurs.idUser'), primary_key=True, nullable=False),
    Column('idCategorie', ForeignKey('Categorie.idCategorie'), primary_key=True, nullable=False, index=True),
    Index('idUser', 'idUser', 'idCategorie')
)


class Coffre(Base):
    __tablename__ = 'Coffre'

    idCoffre = Column(INTEGER(11), primary_key=True)
    idCategorie = Column(ForeignKey('Categorie.idCategorie'), index=True)
    email = Column(String(255), nullable=False)
    password = Column(String(512), nullable=False)
    urlsite = Column(String(512), nullable=False)
    urllogo = Column(String(512), nullable=False)
    note = Column(String(512), nullable=False)

    Categorie = relationship('Categorie')
    Utilisateurs = relationship('Utilisateur', secondary='Classeur')

class Classeur(Base):
    __tablename__ = 'Classeur'

    idUser = Column(ForeignKey('Utilisateurs.idUser'), primary_key=True, nullable=False)
    idCoffre = Column(ForeignKey('Coffre.idCoffre'), primary_key=True, nullable=False, index=True)

    Coffre = relationship('Coffre')
    Utilisateurs = relationship('Utilisateur')


# t_Classeur = Table(
#     'Classeur', metadata,
#     Column('idUser', ForeignKey('Utilisateurs.idUser'), primary_key=True, nullable=False),
#     Column('idCoffre', ForeignKey('Coffre.idCoffre'), primary_key=True, nullable=False, index=True),
#     Index('idUser', 'idUser', 'idCoffre')
# )
