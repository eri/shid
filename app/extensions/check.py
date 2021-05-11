from . import mongo
import random

def generer_identifiant(nom, prenom):
    """
    Permet de générer un identifiant avec vérifications
    - Structure par défaut: <prenom>.<nom>(chiffre)
    - Prenom: Premier prénom uniquement
    - Nom: Trois premières lettres uniquement, sans espaces
    - Chiffre: Faculatatif, ajouté si conflit avec autre id
    """

    identifiant = f"{prenom.split(' ')[0]}.{nom.replace(' ')[:3]}"
    user_db = mongo.find("shid", "soignants", {"id": identifiant})

    if user_db or user_db.count() > 0:
        identifiant += str(random.randint(0, 9))
        return identifiant

    return identifiant
