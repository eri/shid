import datetime

MONGODB_URI = "mongodb://mongodb:27017"
MONGODB_DEV_URI = "mongodb://localhost:27017"

DEFAULT_COLLECTION_DEPARTEMENTS = [
    {"nom": "Urgences", "id": "00001", "image": ""},
    {"nom": "Réanimation", "id": "00002", "image": ""},
    {"nom": "Admissions", "id": "00003", "image": ""},
    {"nom": "Dentaire", "id": "00004", "image": ""},
    {"nom": "Orthodentie", "id": "00005", "image": ""},
    {"nom": "Cardiologie", "id": "00006", "image": ""},
    {"nom": "Radiologie", "id": "00007", "image": ""},
    {"nom": "Technique", "id": "00008", "image": ""},
]

DEFAULT_COLLECTION_ROLES = [
    {
        "nom": "Administrateur", 
        "id": "00001", 
        "permissions": ["ADMINISTRATEUR"]
    },
    {
        "nom": "Médecin", 
        "id": "00002", 
        "permissions": [
            "AFFICHER_STATS", 
            "AJOUTER_DOSSIER_ALL", 
            "AFFICHER_DOSSIER_ALL", 
            "EDITER_DOSSIER_DEP", 
            "SUPPRIMER_DOSSIER_DEP",
        ]
    },
    {
        "nom": "Urgentiste", 
        "id": "00003", 
        "permissions": [
            "AFFICHER_STATS", 
            "AJOUTER_DOSSIER_DEP", 
            "AFFICHER_DOSSIER_DEP", 
            "EDITER_DOSSIER_DEP",
        ]
    },
    {
        "nom": "Infirmier", 
        "id": "00004", 
        "permissions": [
            "AFFICHER_STATS",
            "AFFICHER_DOSSIER_DEP", 
            "EDITER_DOSSIER_DEP",
        ]
    },
    {
        "nom": "Ambulancier", 
        "id": "00005", 
        "permissions": [
            "AFFICHER_STATS",
            "AFFICHER_DOSSIER_DEP", 
        ]
    },
    {
        "nom": "Secrétaire", 
        "id": "00006", 
        "permissions": [
            "AJOUTER_DOSSIER_DEP", 
            "AFFICHER_DOSSIER_DEP", 
            "EDITER_DOSSIER_DEP", 
            "SUPPRIMER_DOSSIER_DEP",         
        ]
    },
]

DEFAULT_COLLECTION_STRUCTURE = [
    {
        "id": "configuration",
        "setup": False,
        "structure": {
            "type":         "",
            "nom":          "",
            "adresse":      "",
            "code_postal":  "",
            "ville":        "",
        },
        "covid_mode": {
            "enabled": False,
            "daily_dose": ""
        }
    },
    {
        "id": "permissions",
        "values": [
            "ADMINISTRATEUR",        # Toutes les permissions + configuration structure
            "AFFICHER_STATS",        # Stats générales de la structure sur la page d'accueil
            "AJOUTER_DOSSIER_ALL", 
            "AJOUTER_DOSSIER_DEP", 
            "AFFICHER_DOSSIER_ALL",  # ALL = Ensemble
            "AFFICHER_DOSSIER_DEP",  # DEP = Département uniquement
            "AFFICHER_DOSSIER_PER",  # PER = Seulement assigné          
            "EDITER_DOSSIER_ALL",
            "EDITER_DOSSIER_DEP",
            "EDITER_DOSSIER_PER",
            "SUPPRIMER_DOSSIER_ALL",
            "SUPPRIMER_DOSSIER_DEP",
            "SUPPRIMER_DOSSIER_PER",
        ],
    },
]

DEFAULT_COLLECTION_PATIENT = {
    "id": "00001",
    "sexe": "masculin",
    "nom": "Dupont",
    "prenom": "Paul",
    "date_naissance": "01/01/1990",
    "adresse": "21 Rue du Patient de l'Exemple",
    "code_postal": "75000",
    "ville": "Paris",
    "telephone": "0607080910",
    "email": "exemple@mail.com",
    "date_enregistrement": datetime.datetime.now(),
    "numero_ss": "1 23 45 67 890 123 45",
    "dossiers": [
        {
            "id": "00001",
            "date": datetime.datetime.now(),
            "departements": ["00001", "00002"],
            "historique": [
                {
                    "id": "00001",
                    "date": datetime.datetime.now(),
                    "description": "[Exemple] Passage aux urgences suite à un accident de la route",
                    "departement": {
                        "id": "00001",
                        "nom": "Urgences",
                    },
                    "personnel": {
                        "id": "00002",
                        "nom": "Fevre",
                        "prenom": "Catherine"
                    },
                },
            ]
        }
    ]
}

DEFAULT_COLLECTION_PERSONNELS = {
        "id": "00002",
        "sexe": "feminin",
        "nom": "Fevre",
        "prenom": "Catherine",
        "nom_utilisateur": "fevre.cat",
        "mot_passe": "",
        "roles": ["00002", "00003"],
        "departements": ["00001"],
        "date_naissance": "21/03/1989",
        "date_enregistrement": str(datetime.datetime.now()),
        "numero_ss": "1 08 787 982 81"
}
