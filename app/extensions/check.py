import extensions.mongo as mongo

import random
import pymongo

def dernier_id(collection):
    """Retourne le dernier identifiant pour la collection sélectionnée"""
    query = mongo.find_sorted('shid', collection, {}, {"k": "id", "o": pymongo.DESCENDING})[0]
    identifiant = int(query['id'])+1
    return f"000{identifiant}"

def generer_identifiant(nom, prenom):
    """
    Permet de générer un identifiant avec vérifications
    - Structure par défaut: <prenom>.<nom>(chiffre)
    - Prenom: Premier prénom uniquement
    - Nom: Trois premières lettres uniquement, sans espaces
    - Chiffre: Faculatatif, ajouté si conflit avec autre id
    """

    identifiant = f"{prenom.lower().split(' ')[0]}.{nom.lower().replace(' ', '')[:3]}"
    user_db = mongo.find("shid", "soignants", {"nom_utilisateur": identifiant})

    if user_db:
        identifiant += str(random.randint(0, 9))
        return identifiant

    return identifiant
