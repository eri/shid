from flask import (
    Flask,
    render_template,
    send_from_directory,
    jsonify,
    redirect,
    request,
    session,
    url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_caching import Cache

import extensions.mongo as mongo
import extensions.check as check
import extensions.data as data

import datetime
import requests
import pymongo
import string
import random
import os

# Set our Flask config
config = {
    "DEBUG": True,  # Flask debugging
    "CACHE_TYPE": "simple",  # Flask cache - type
    "CACHE_DEFAULT_TIMEOUT": 200,  # Flask cache - default cache expire timeout
    "TEMPLATES_AUTO_RELOAD": True,  # Auto reload Flask
    "SECRET_KEY": "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(50)]
    )
}

# Define the Flask Application
app = Flask(__name__, static_url_path="/", static_folder="static", template_folder="templates")
app.config.from_mapping(config)

# Define other dependencies
# cache = Cache(app)
# cache.init_app(app)

@app.before_first_request
def verification_bdd():
    """Vérifie que la connexion à la base de données est établie"""
    try:
        mongo_client = pymongo.MongoClient("mongodb://mongodb:27017")
        mongo_client.server_info()
        print("Connexion réussi à MongoDB sur localhost:27017 !")
        
        print("Création de la base de donnée et des collections...")
        db = mongo_client["shid"]
        col_patients = db['patients']
        col_soignants = db['soignants']
        col_departements = db['departements']
        col_roles = db['roles']
        col_structure = db['structure']
        
        print("Base de données et collection crée!")

    except Exception as e:
        print(f"Connexion à MongoDB échoué... Erreur: `{e}`")

@app.route("/")
@app.route("/login/")
@app.route("/accueil/")
def index():
    """Retourne la page d'accueuil du site"""
    if pymongo.MongoClient("mongodb://mongodb:27017")['shid']['structure'].find({}).count() == 0:
        return render_template("views/setup.html")

    if "USER" in session:
        # Utilisateur est connecté
        return render_template("views/accueil.html")

    # L'utilisateur n'est pas connecté, retour au login
    return render_template("views/login.html", **{'data':data})

@app.route("/500/")
def unauthorized():
    """Retourne la page d'accueuil du site"""
    return render_template("views/500.html")

@app.route("/setup/")
def setup_page():
    """Retourne la page d'accueuil du site"""
    return render_template("views/setup.html")


@app.route("/profil/")
def profil():
    """Retourne la page d'accueuil du site"""
    return render_template("views/profil.html")


@app.route("/dossiers/")
def liste_dossiers_patients():
    """Affiche les dossiers des patients du département concerné"""
    return render_template("views/liste_dossiers.html")


@app.route("/dossiers/nouveau/")
def nouveau_dossier_patient():
    """Crée un nouveau dossier pour un patient"""
    return render_template("views/ajout_dossier.html", **{'data':data})


@app.route("/dossiers/<id>/")
def dossier_patient(id):
    """Affiche un dossier patient en particulier"""
    dossier = data.get_dossier(id)

    if not dossier:
        return jsonify(
            { "success": False, "code": 404, "error": "Dossier introuvable."}
        )
    
    patient = dossier
    dossier = patient['dossiers'][str(id)]
    dossier['id'] = str(id)

    donnees = {
        "dossier": dossier,
        "patient": patient,
        "departements": [data.get_departement(d) for d in dossier['departements']],
        "personnels": [data.get_soignant(p) for p in dossier['personnels_assignes']],
        "historique": dossier['historique'],
    }
    return render_template("views/dossier.html", **{"d":donnees})


@app.route("/admin/personnels/")
def liste_personnels():
    """Affiche la liste des personnels du département concerné"""
    return render_template("views/liste_personnel.html")

@app.route("/admin/personnels/nouveau")
def ajout_personnel():
    """Ajouter un personnel dans la base de données"""
    return render_template("views/ajout_personnel.html")

@app.route("/admin/")
def portail_administration():
    """Affiche la page d'administration de la structure hospitalière"""
    return render_template("views/admin.html", **{'data':data})

# @app.route("/admin/departement/<name>/")
# def page_departement(name):
#     """Affiche la page de gestion d'un département"""
#     return render_template("views/admin.html")

# @app.route("/admin/role/<name>/")
# def page_role(name):
#     """Affiche la page de gestion d'un role"""
#     return render_template("views/admin.html")

@app.route("/github/")
def github():
    """Retourne la page d'accueuil du site"""
    return redirect("https://github.com/eri/shid")

@app.route("/api/auth/setup/")
def setup_screen():
    """Réalise le démarrage rapide dans la base de données"""
    
    type_structure = str(request.args.get('type_structure')).strip()
    nom_structure = str(request.args.get('nom_structure')).strip()
    adresse_structure = str(request.args.get('adresse_structure')).strip()
    cp_structure = str(request.args.get('cp_structure')).strip()
    ville_structure = str(request.args.get('ville_structure')).strip()

    covid_structure = str(request.args.get('covid_structure')).strip()
    covid_dose = str(request.args.get('covid_dose')).strip()
    capacite_lit = str(request.args.get('capacite_lit')).strip()

    username_admin = str(request.args.get('username_admin')).strip()
    password_admin = str(request.args.get('password_admin')).strip()
    email_admin = str(request.args.get('email_admin')).strip()
    public_stats = str(request.args.get('public_stats')).strip()

    data = {
        "type": "settings",
        "type_structure": type_structure,
        "nom_structure": nom_structure,
        "adresse_structure": adresse_structure,
        "cp_structure": cp_structure,
        "ville_structure": ville_structure,
        "covid_structure": covid_structure,
        "covid_dose": covid_dose,
        "capacite_lit": capacite_lit,
        "public_stats": public_stats,
    }

    admin_account = {
        "id": check.dernier_id("soignants"),
        "sexe": "",
        "nom": "Administrateur",
        "prenom": "",
        "nom_utilisateur": username_admin,
        "mot_passe": generate_password_hash(password_admin),
        "roles": ["0012"],
        "departements": ["0002"],
        "date_naissance": "",
        "date_enregistrement": datetime.datetime.now(),
        "numero_ss": "",
        "adresse_email": email_admin
    }

    try:
        admin_db = mongo.insert_one("shid", "soignants", admin_account)
        settings_db = mongo.insert_one("shid", "structure", data)

        return jsonify(
            {"success": True,
            "message": f"Setup terminée avec succès. Votre compte administrateur à été généré sous le nom d'utilisateur <b>{admin_account['nom_utilisateur']}</b> et le mot de passe associé. Cliquer sur le bouton pour vous connecter."}
        )
    except Exception as e:
        return jsonify(
            {
                "success": False,
                "error": f"Erreur interne survenue lors de la communication avec la base de donnée. {e}",
            }
        )

@app.route("/api/auth/login/")
def login():
    """Authentifie un utilisateur et crée une session"""
    identifiant = str(request.args.get('username')).strip()
    mdp = str(request.args.get('password')).strip()
    
    try:
        user_db = mongo.find("shid", "soignants", {"nom_utilisateur": identifiant})
    except Exception as e:
        return jsonify(
            {"success": False, "error": f"Erreur interne. Veuillez réessayer dans quelques minutes. Si cela persiste, contactez l'administrateur de votre structure. Reférence: {e}"}
        )       

    if not user_db:
        # L'utilisateur n'existe pas
        return jsonify(
            {"success": False, "error": "Identifiant invalide ou n'existe pas."}
        )

    if check_password_hash(user_db[0]["mot_passe"], mdp):
        # On vérifie si le hash du mot de passe enregistré en BDD
        # corresponds avec le mot de passe en clair en toute sécurité
        session["USER"] = identifiant
        return jsonify(
            {"success": True, "message": "Mot de passe correct. Redirection..."}
        )

    return jsonify(
        {"success": False, "error": "Mot de passe incorrect. Vérifiez la saisie."}
    )


@app.route("/api/auth/register/")
def register():
    """Enregistre un utilisateur dans la base de données"""
    nom = str(request.args.get('nom')).strip()
    prenom = str(request.args.get('prenom')).strip()
    departement = str(request.args.get('departement')).strip()
    role = str(request.args.get('role')).strip()

    mdp = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(12)]
    )
    date_naissance = datetime.datetime.strptime(
        str(request.args.get('date_naissance')).strip(), "%Y-%m-%d"
    )

    data = {
        "id": check.dernier_id("soignants"),
        "sexe": str(request.args.get('sexe')).strip(),
        "nom": nom,
        "prenom": prenom,
        "nom_utilisateur": check.generer_identifiant(nom, prenom),
        "mot_passe": generate_password_hash(mdp),
        "roles": [f"{role}"],
        "departements": [f"{departement}"],
        "date_naissance": date_naissance,
        "date_enregistrement": datetime.datetime.now(),
        "numero_ss": str(request.args.get('numero_ss')).strip(),
        "adresse_email": str(request.args.get('adresse_email')).strip()
    }

    try:
        user_db = mongo.insert_one("shid", "soignants", data)
        return jsonify(
            {"success": True,
            "message": f"Compte crée avec succès. Le nom d'utilisateur est <b>{data['nom_utilisateur']}</b> et le mot de passe généré est <b>{mdp}</b>. Veillez à bien le noter, il ne sera plus possible de le récupérer ulterieurement."}
        )
    except Exception as e:
        return jsonify(
            {
                "success": False,
                "error": f"Erreur survenue lors de la création du compte. {e}",
            }
        )


@app.route("/api/logout/")
def logout():
    """Authentifie un utilisateur et crée une session"""
    session.pop("USER", None)
    return redirect("/")


@app.route("/api/stats/")
def stats():
    """Retourne les résultats des statistiques depuis la base de données"""

    lits_disponibles = mongo.find("shid", "parametres", {"type": "capacité"})[0]["lits"]
    hospitalisations = mongo.find(
        "shid", "patients", {"departement": "hospitalisation"}
    ).count()
    reanimation = mongo.find("shid", "patients", {"departement": "réanimation"}).count()
    urgences = mongo.find("shid", "patients", {"departement": "urgences"}).count()

    return jsonify(
        {
            "lits": lits_disponibles,
            "hospitalisations": hospitalisations,
            "reanimation": reanimation,
            "urgences": urgences,
        }
    )


@app.route("/api/search/<type>/<query>/")
def search_db(type, query):
    """Recherche les patients et soignants par nom/prenom"""
    search = mongo.find(
        "shid",
        type,
        {
            "$or": [
                {"nom": {"$regex": query, "$options": "i"}},
                {"prenom": {"$regex": query, "$options": "i"}},
            ]
        },
    )
    return search

@app.context_processor
def checkers():
    def active_session():
        return True if "USER" in session else False

    def session_user():
        if not "USER" in session: return False
        return data.get_soignant_by_username(session['USER'])

    def resolve_departement(id):
        return data.get_departement(id)

    def resolve_all_departements():
        return data.get_all_departements()

    def resolve_all_roles():
        return data.get_all_roles()

    def get_data():
        return data

    return dict(
        active_session=active_session,
        session_user=session_user,
        resolve_departement=resolve_departement,
        get_data=get_data,
        resolve_all_departements=resolve_all_departements,
        resolve_all_roles=resolve_all_roles
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
