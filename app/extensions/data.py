import datetime
import extensions.mongo as mongo


STRUCTURE = {
    "type": "hôpital",
    "nom": "Avicennes",
    "admin_mail": "admin@sante.fr"
}

PATIENT = {
    "id": "0001",
    "sexe": "masculin",
    "nom": "Leroy",
    "prenom": "Christophe",
    "date_naissance": "12/09/1985",
    "adresse": "112 Avenue de la République",
    "code_postal": "75020",
    "ville": "Paris",
    "numero_tel": "06 12 34 56 78",
    "adresse_mail": "leroy.christophe@gmail.com",
    "date_enregistrement": str(datetime.datetime.now()),
    "numero_ss": "1 03 457 897 86",
    "dossiers": {
        "0002" : {
            "date": str(datetime.datetime.now()),
            "departements": ["0003", "0006"],
            "personnels_assignes": ["0005", "0006"],
            "historique": [
                {
                    "id": "0007",
                    "date": str(datetime.datetime.now()),
                    "departement": "0001",
                    "soignant": "0005",
                    "description": "Passage aux urgences suite à un accident de la route"
                },
                {
                    "id": "0011",
                    "date": str(datetime.datetime.now()),
                    "departement": "0006",
                    "soignant": "0006",
                    "description": "Radio du rachis cervical suite aux douleurs intenses"
                }
            ]
        }
    }
}

SOIGNANT = [
    {
        "id": "0005",
        "sexe": "feminin",
        "nom": "Fevre",
        "prenom": "Catherine",
        "roles": ["0013", "0014"],
        "departements": ["0001"],
        "date_naissance": "21/03/1989",
        "date_enregistrement": str(datetime.datetime.now()),
        "numero_ss": "1 08 787 982 81"
    },
    {
        "id": "0006",
        "sexe": "masculin",
        "nom": "Valois",
        "prenom": "Fredéric",
        "roles": ["0013"],
        "departements": ["0006"],
        "date_naissance": "09/04/1987",
        "date_enregistrement": str(datetime.datetime.now()),
        "numero_ss": "1 02 187 582 15"
    },
]

DEPARTEMENTS = [
    {"nom": "Urgences", "id": "0001", "image": ""},
    {"nom": "Admissions", "id": "0002", "image": ""},
    {"nom": "Dentaire", "id": "0003", "image": ""},
    {"nom": "Orthodentie", "id": "0004", "image": ""},
    {"nom": "Cardiologie", "id": "0005", "image": ""},
    {"nom": "Radiologie", "id": "0006", "image": ""},
]

ROLES = [
    {"nom": "Administrateur", "id": "0012"},
    {"nom": "Médecin", "id": "0013"},
    {"nom": "Urgentiste", "id": "0014"},
    {"nom": "Infirmier", "id": "0015"},
    {"nom": "Ambulancier", "id": "0016"},
    {"nom": "Secrétaire", "id": "0017"},
]

def get_departement(id):
    return mongo.find("shid", "departements", {"id":str(id)})[0]

def get_all_departements():
    return mongo.find("shid", "departements", {})

def get_role(id):
    return mongo.find("shid", "departements", {"id":str(id)})[0]

def get_all_roles():
    return mongo.find("shid", "roles", {})

def get_soignant(id):
    return mongo.find("shid", "soignants", {"id":str(id)})[0]

def get_soignant_by_username(name):
    query = mongo.find("shid", "soignants", {"nom_utilisateur":name})[0]
    return False if not query else {"nom":query['nom'], "prenom":query['prenom']}

def get_patient(id):
    return mongo.find("shid", "patients", {"id":str(id)})[0]
    
def get_dossier(id):
    return mongo.find("shid", "patients", {f"dossiers.{id}":{"$exists": True}})[0]

def get_historique(id):
    return dict(mongo.find("shid", "patients", {f"dossiers.{id}":{"$exists": True}}))[0]
    

def datetime_object(date):
    return datetime.datetime.strptime(date, '%d/%m/%Y')