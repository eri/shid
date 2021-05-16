import datetime

import extensions.config as config
import extensions.mongo as client


def verify_db_connection():
    """Vérifie si la connexion entre MongoDB-Flask est bien établie"""
    try:
        # Tente de prendre les informations du serveur
        client.mongo.server_info()
        return {
            "success": True,
            "message": f"Connexion réussi à MongoDB sur {config.MONGODB_URI}."
        }
    except Exception as e:
        return {
            "success": False,
            "code": 503,
            "time": str(datetime.datetime.now()).split(" ")[1],
            "message": e
        } 

def is_setup():
    """Vérifier si la base de donnée à bien été mise en place"""
    return False if client.mongo['shid']['structure'].find({}).count() == 0 else True

def initialize_db():
    """Crée la base de donnée et les collections"""

    print("Création de la base de donnée et des collections...")

    # Database
    db = client.mongo["shid"]
    # Collections
    col_patients = db['patients'].insert_one(config.DEFAULT_COLLECTION_PATIENT)
    col_personnels = db['personnels'].insert_one(config.DEFAULT_COLLECTION_PERSONNELS)
    col_departements = db['departements'].insert_many(config.DEFAULT_COLLECTION_DEPARTEMENTS)
    col_roles = db['roles'].insert_many(config.DEFAULT_COLLECTION_ROLES)
    col_structure = db['structure'].insert_many(config.DEFAULT_COLLECTION_STRUCTURE)
    
    print("Base de données et collections crée, données par défaut insérés!")
    