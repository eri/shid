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
    except Exception as e:
        webhook.send(f"Connexion à MongoDB échoué... Erreur: `{e}`")

@app.route("/")
@app.route("/login")
def index():
    """Retourne la page d'accueuil du site"""
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

@app.route("/accueil/")
def logged_in():
    """Retourne la page d'accueuil du site"""
    return render_template("views/accueil.html")


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
    return render_template("views/ajout_dossier.html")


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


@app.route("/admin/")
def portail_administration():
    """Affiche la page d'administration de la structure hospitalière"""
    return render_template("views/admin.html", **{'data':data})

@app.route("/admin/departement/<name>/")
def page_departement(name):
    """Affiche la page de gestion d'un département"""
    return render_template("views/admin.html")

@app.route("/admin/role/<name>/")
def page_role(name):
    """Affiche la page de gestion d'un role"""
    return render_template("views/admin.html")

@app.route("/github/")
def github():
    """Retourne la page d'accueuil du site"""
    return redirect("https://github.com/eri/shid")

@app.route("/api/login/")
def login():
    """Authentifie un utilisateur et crée une session"""
    identifiant = str(request.form["identifiant"]).strip()
    mdp = request.form["motdepasse"]

    user_db = mongo.find("shid", "soignants", {"identifiant": identifiant})

    if not user_db or user_db.count() <= 0:
        # L'utilisateur n'existe pas
        return jsonify(
            {"success": False, "error": "Identifiant invalide ou n'existe pas."}
        )

    if check_password_hash(user_db["password"], mdp):
        # On vérifie si le hash du mot de passe enregistré en BDD
        # corresponds avec le mot de passe en clair en toute sécurité
        session["USER"] = identifiant
        return jsonify(
            {"success": True, "message": "Mot de passe correct. Redirection..."}
        )

    return jsonify(
        {"success": False, "error": "Mot de passe incorrect. Vérifiez la saisie."}
    )


@app.route("/api/register/")
def register():
    """Enregistre un utilisateur dans la base de données"""

    sexe = str(request.form["sexe"]).strip()
    nom = str(request.form["nom"]).strip()
    prenom = str(request.form["prenom"]).strip()
    identifiant = check.generer_identifiant(nom, prenom)
    mdp = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(12)]
    )
    date_naissance = datetime.datetime.strptime(
        str(request.form["date_naissance"]).strip(), "%d/%m/%Y"
    )

    data = {
        "sexe": sexe,
        "nom": nom,
        "prenom": prenom,
        "identifiant": identifiant,
        "password": generate_password_hash(mdp),
        "date_naissance": date_naissance,
    }
    try:
        user_db = mongo.insert_one("shid", "soignants", data)
        return jsonify(
            {"success": True, "message": "Compte crée avec succès.", "data": user_db}
        )
    except Exception:
        return jsonify(
            {
                "success": False,
                "error": "Erreur survenue lors de la création du compte.",
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
    def resolve_departement(id):
        return data.get_departement(id)

    return dict(resolve_departement=resolve_departement)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
