from flask import (
    Flask,
    render_template,
    send_from_directory,
    jsonify,
    redirect,
    request,
    session,
    url_for,
    abort
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_caching import Cache

import extensions.mongo as mongo
import extensions.check as check
import extensions.data as data
import extensions.setup as setup

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

### Definir l'application Flask
app = Flask(__name__, static_url_path="/", static_folder="static", template_folder="templates")
app.config.from_mapping(config)

### Définir le cache côté serveur
cache = Cache(app)
cache.init_app(app)

### Vérification avant les requêtes
def is_active_session():
    return False if setup.is_setup() and not "USER" in session else True

@app.before_first_request
def first_setup():
    """Vérifications avant de traiter la première requête"""
    if not setup.is_setup():
        setup.initialize_db()

@app.before_request
def login_session_check():
    """Vérifie que l'utilisateur est bien dans une session active."""
    db_check = setup.verify_db_connection()
    if not db_check['success']:
        return render_template("views/errors/503.html", **{"e":db_check}), 503

@app.route("/")
def index():
    """Page d'accueil du site"""
    if not setup.is_setup():
        return render_template("views/setup.html")

    if not is_active_session(): return render_template("views/login.html")

    return render_template("views/accueil.html")

# @app.route("/profil/")
# def profil():
#     """Retourne la page d'accueuil du site"""
#     return render_template("views/profil.html")

### Dossiers patient

@app.route("/dossiers/")
def liste_dossiers_patients():
    """Affiche les dossiers des patients du département concerné"""
    if not is_active_session(): return redirect(url_for("index"))
    return render_template("views/liste_patients.html")


@app.route("/dossiers/nouveau/")
def nouveau_dossier_patient():
    """Crée un nouveau dossier pour un patient"""
    if not is_active_session(): return redirect(url_for("index"))
    return render_template("views/ajout_dossier.html")

@app.route("/dossiers/<id>/")
def dossier_patient(id):
    """Affiche un dossier patient en particulier"""
    if not is_active_session(): return redirect(url_for("index"))
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

### Partie administration

@app.route("/admin/")
def portail_administration():
    """Affiche la page d'administration de la structure hospitalière"""
    if not is_active_session(): return redirect(url_for("index"))
    return render_template("views/admin.html")

@app.route("/admin/personnels/")
def liste_personnels():
    """Affiche la liste des personnels du département concerné"""
    if not is_active_session(): return redirect(url_for("index"))
    return render_template("views/liste_personnel.html")

@app.route("/admin/personnels/nouveau")
def ajout_personnel():
    """Ajouter un personnel dans la base de données"""
    if not is_active_session(): return redirect(url_for("index"))
    return render_template("views/ajout_personnel.html")

@app.route("/admin/roles/nouveau")
def ajout_role():
    """Ajouter un personnel dans la base de données"""
    if not is_active_session(): return redirect(url_for("index"))
    return render_template("views/ajout_roles.html")

@app.route("/admin/departements/nouveau")
def ajout_departement():
    """Ajouter un personnel dans la base de données"""
    if not is_active_session(): return redirect(url_for("index"))
    return render_template("views/ajout_departement.html")

### Routes API

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

    structure_data = {
        "id": "configuration",
        "setup": True,
        "structure": {
            "type":         type_structure,
            "capacite_lit": capacite_lit,
            "nom":          nom_structure,
            "adresse":      adresse_structure,
            "code_postal":  cp_structure,
            "ville":        ville_structure,
        },
        "covid_mode": {
            "enabled": covid_structure,
            "daily_dose": covid_dose
        }
    }

    admin_account = {
        "id": "00001",
        "sexe": "",
        "nom": "Administrateur",
        "prenom": "",
        "nom_utilisateur": username_admin,
        "mot_passe": generate_password_hash(password_admin),
        "roles": ["00001"],
        "departements": ["00008"],
        "date_naissance": "",
        "date_enregistrement": datetime.datetime.now(),
        "numero_ss": "",
        "adresse_email": email_admin
    }

    try:
        admin_db = mongo.insert_one("shid", "personnels", admin_account)
        settings_db = mongo.replace_one("shid", "structure", {"id": "configuration"}, structure_data)

        return jsonify(
            {"success": True,
            "message": f"Setup terminée avec succès. Votre compte administrateur <b>{admin_account['nom_utilisateur']}</b> et le mot de passe associé. Cliquer sur le bouton pour vous connecter."}
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
        user_db = mongo.find("shid", "personnels", {"nom_utilisateur": identifiant})
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


@app.route("/api/roles/new/")
def api_new_role():
    """Réalise le démarrage rapide dans la base de données"""
    
    nom_role = str(request.args.get('nom_role')).strip()
    permissions = []

    for x in [
        "afficher_stats", 
        "ajouter_dossier", 
        "afficher_dossier", 
        "editer_dossier", 
        "supprimer_dossier"
    ]:
        perm_check = str(request.args.get(x)).strip()
        if not "False" in perm_check: permissions.append(perm_check)

    role_data = {
        "nom": nom_role, 
        "id": check.dernier_id("roles"), 
        "permissions": permissions
    }

    try:
        role_db = mongo.insert_one("shid", "roles", role_data)

        return jsonify(
            {"success": True,
            "message": f"Rôle sauvegardée avec succès."}
        )
    except Exception as e:
        return jsonify(
            {
                "success": False,
                "error": f"Erreur interne survenue lors de la communication avec la base de donnée. {e}",
            }
        )

@app.route("/api/roles/delete/<id>/")
def api_delete_role(id):
    """Supprime un rôle dans la base de données"""
    mongo.delete_one("shid", "roles", {"id":str(id)})
    return redirect(url_for('portail_administration'))


@app.route("/api/departements/new/")
def api_new_departement():
    """Ajoute un département dans la base de données"""
    
    nom_dep = str(request.args.get('nom_departement')).strip()
    dep_data = {"nom": nom_dep, "id": check.dernier_id("departements"), "image":""}

    try:
        dep_db = mongo.insert_one("shid", "departements", dep_data)
        return jsonify({"success": True,
            "message": f"Département sauvegardée avec succès."})
    except Exception as e:
        return jsonify({"success": False,
                "error": f"Erreur interne survenue lors de la communication avec la base de donnée. {e}"})

@app.route("/api/departements/delete/<id>/")
def api_delete_departement(id):
    """Supprime un rôle dans la base de données"""
    mongo.delete_one("shid", "departements", {"id":str(id)})
    return redirect(url_for('portail_administration'))

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
    search = {}
    return search

### Redirections

@app.route("/github/")
def github():
    """Lien vers le repository GitHub du projet"""
    return redirect("https://github.com/eri/shid")

### Pages d'erreur personnalisées

@app.errorhandler(403)
def page_not_found(e):
    """Erreur 403 - Non autorisé"""
    return render_template('views/errors/403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    """Erreur 404 - Page introuvable"""
    return render_template('views/errors/404.html'), 404

@app.errorhandler(503)
def service_unavailable():
    """Erreur 503 - Service non disponible"""
    return render_template("views/errors/503.html"), 503

### Processeur de contexte global

@app.context_processor
def checkers():
    def active_session():
        return True if "USER" in session else False

    def session_user():
        user_ses = data.get_soignant_by_username(session['USER'])
        return user_ses

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
