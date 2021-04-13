from flask import Flask, render_template, send_from_directory, jsonify, redirect, request, session
from flask_caching import Cache

import requests
import pymongo
import os

# Set our Flask config
config = {
    "DEBUG": True,                  # Flask debugging
    "CACHE_TYPE": "simple",         # Flask cache - type
    "CACHE_DEFAULT_TIMEOUT": 200,   # Flask cache - default cache expire timeout
    "TEMPLATES_AUTO_RELOAD": True,  # Auto reload Flask
}

# Define the Flask Application
app = Flask(__name__, static_url_path='/', static_folder='static', template_folder='templates')
app.config.from_mapping(config)

# Define other dependencies
cache = Cache(app)
cache.init_app(app)

# @app.before_first_request
# def verification_bdd():
#     """Vérifie que la connexion à la base de données est établie"""
#     try:
#         mongo = pymongo.MongoClient("localhost", 27017, serverSelectionTimeoutMS=100)
#         mongo.server_info()
#         print(f"Connexion réussi à MongoDB sur localhost:27017 !")
#     except Exception:
#         print("Connexion à MongoDB échoué... Vérifiez les logs du Docker et redémarrez.")
#         exit()

@app.route('/')
@app.route('/login')
def index():
    """Retourne la page d'accueuil du site"""
    if "USER" in session:
       # Utilisateur est connecté 
        return render_template("views/accueil.html")
    
    # L'utilisateur n'est pas connecté, retour au login
    return render_template("views/login.html")

@app.route('/accueil/')
def logged_in():
    """Retourne la page d'accueuil du site"""
    return render_template("views/accueil.html")
    
@app.route('/dossiers/')
def dossiers_patients():
    """Affiche les dossiers des patients du département concerné"""
    return render_template("views/liste_dossiers.html")

@app.route('/dossier/')
def dossiers_patients():
    """Affiche les dossiers des patients du département concerné"""
    return render_template("views/dossier.html")

@app.route('/admin/')
def portail_administration():
    """Affiche la page d'administration de la structure hospitalière"""
    return render_template("views/admin.html")

@app.route('/api/stats/')
@cache.cached(timeout=60)
def stats():
    """Retourne les résultats des statistiques depuis la base de données"""

    lits_disponibles = mongo['shid']['parametres'].find({"type" : "capacité"})[0]['lits']
    hospitalisations = mongo['shid']['patients'].find({"departement" : "hospitalisation"}).count()
    reanimation = mongo['shid']['patients'].find({"departement" : "réanimation"}).count()
    urgences = mongo['shid']['patients'].find({"departement" : "urgences"}).count()

    return jsonify({"lits" : lits_disponibles,
                    "hospitalisations" : hospitalisations,
                    "reanimation" : reanimation,
                    "urgences" : urgences })

@app.route('/api/search/<type>/<query>/')
def search_db(type, query):
    """Recherche les patients et soignants par nom/prenom"""
    search = mongo['shid'][type].find({
            "$or": [
                { "nom": { '$regex': query, '$options': 'i' } },
                { "prenom": { '$regex': query, '$options': 'i' } }
            ]})
    return search

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")