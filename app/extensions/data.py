import datetime
import extensions.mongo as mongo

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
    return False if not query else query

def get_patient(id):
    return mongo.find("shid", "patients", {"id":str(id)})[0]
    
def get_dossier(id):
    return mongo.find("shid", "patients", {f"dossiers.{id}":{"$exists": True}})[0]

def get_historique(id):
    return dict(mongo.find("shid", "patients", {f"dossiers.{id}":{"$exists": True}}))[0]

def structure():
    return mongo.find("shid", "structure", {})[0]

def stats():
    param_structure = structure()
    lits_utilises = mongo.find("shid", "patients", {})
    if not lits_utilises:
        lits_utilises = 0
    else:
        lits_utilises = lits_utilises.count()

    lits_disponibles = int(param_structure['capacite_lit'])-lits_utilises
    doses_disponibles = param_structure['covid_dose']

    patients_urgences = mongo.find("shid", "patients", {})
    if not patients_urgences:
        patients_urgences = 0
    else:
        patients_urgences = patients_urgences.count()

    soignants_rea = mongo.find("shid", "soignants", {'departements.0': '0001'})
    if not soignants_rea:
        soignants_rea = 0
    else:
        soignants_rea = soignants_rea.count()

    return {"1":lits_disponibles, "2":doses_disponibles, "3":lits_utilises, "4": soignants_rea}

def datetime_object(date):
    return datetime.datetime.strptime(date, '%d/%m/%Y')
