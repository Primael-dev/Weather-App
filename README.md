# Weather App

Auteur 

BANKOLE Primael M. William

Licence 

Ce projet est sous licence MIT.

---

## Description

Cette application météo permet de consulter les prévisions météorologiques de n'importe quelle ville dans le monde. Le projet utilise Flask pour le backend et une interface web moderne pour le frontend. Les données météo sont récupérées via l'API Open-Meteo et les coordonnées géographiques via l'API Nominatim d'OpenStreetMap.

---

## Fonctionnalités

- Recherche de prévisions météo par nom de ville
- Affichage des températures maximales et minimales
- Prévisions sur 7 jours
- Interface utilisateur moderne avec effets glassmorphism
- Animation de chargement avec nuage et pluie
- Sauvegarde automatique de l'historique des recherches dans une base de données SQLite
- Affichage automatique de la dernière ville recherchée au chargement

---

## Installation

1.  Ouvrez votre terminal et naviguez vers le dossier du projet **`Weather_App`**.

2.  Créez un environnement virtuel pour le projet :
```bash
    python -m venv env
```

3.  Activez cet environnement :
    * **Sur Windows :**
```bash
        env\Scripts\activate
```
    * **Sur macOS ou Linux :**
```bash
        source env/bin/activate
```

4.  Installez les modules nécessaires à l'exécution du programme à l'aide du fichier `requirements.txt` :
```bash
    pip install -r requirements.txt
```

---

## Utilisation

Une fois l'installation terminée et l'environnement activé, lancez l'application en exécutant la commande suivante dans le terminal :
```bash
python app.py 
```

L'application sera accessible à l'adresse : `http://127.0.0.1:5000`

Ouvrez simplement le fichier `index.html` dans votre navigateur ou accédez à l'interface web pour commencer à rechercher des villes.

---

## Structure du Projet
```
Weather_App/
│
├── app.py                  # Serveur Flask : Point d'entrée principal
├── weather.db              # Base de données SQLite (gérée automatiquement)
│
├── routes/
│   └── api.py              # Définition des points de terminaison (GET/POST)
│
├── core/                   # Moteur logique de l'application
│   ├── getLocation.py      # Géocodage : Convertit une ville en coordonnées
│   ├── getApi.py           # Récupération : Appel HTTP vers Open-Meteo
│   ├── treat_response.py   # Transformation : Nettoyage et ajout des emojis
│   └── cleaner.py          # Orchestration : Coordonne getApi et treat_response
│
├── database/
│   └── saver.py            # Persistance : CRUD pour SQLite
│
└── frontend/               # Interface Utilisateur
    ├── index.html          # Structure HTML5 avec bouton Localisation
    ├── style.css           # Design Glassmorphism & Animations
    ├── app.js              # Logique JS : Fetch, DOM et Navigator Geolocation
    ├── messages/           # Illustrations (404, recherche vide)
    └── weather/            # Icônes météo dynamiques (SVG)

    
```

---

## Itinéraires de l'API

| Verbe | URL | Description | Réponse réussie | Réponse erreur |
|-------|-----|-------------|----------------|----------------|
| GET | /api/weather | Récupère tout l'historique météo | 200 + {"status": "success", "data": [...]} | 500 |
| POST | /api/weather | Ajoute une recherche météo | 201 + {"status": "success", "data": {...}} | 400 / 404 / 500 |

---

## Exemple de Corps de Requête (Payload)

La route POST `/api/weather` attend un corps de requête au format JSON.

### Recherche par nom de ville :
```json
{
    "city": "Paris"
}
```

### Recherche par coordonnées GPS :
```json
{
    "lat": 48.8566,
    "lon": 2.3522,
    "city": "Paris"
}
```

---

## Exemple de Réponse
```json
{
    "status": "success",
    "data": [
        {
            "date": "2025-12-26",
            "max": 15.5,
            "min": 8.2,
            "state": "Partiellement nuageux ⛅",
            "city": "Paris"
        },
        {
            "date": "2025-12-27",
            "max": 14.0,
            "min": 7.5,
            "state": "Pluie légère 🌦️",
            "city": "Paris"
        }
    ]
}
```

---

## Technologies Utilisées

### Backend
- Python 3.x
- Flask
- SQLite3
- Requests
- Geocoder

### Frontend
- HTML5
- CSS3 (avec animations et glassmorphism)
- JavaScript (Vanilla)
- Google Fonts (Poppins)
- Material Symbols

### APIs Externes
- Open-Meteo API (données météorologiques)
- Nominatim OpenStreetMap (géocodage)

---

## Base de Données

L'application utilise SQLite pour stocker l'historique des recherches météo.

### Structure de la table `previsions` :

| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER | Clé primaire auto-incrémentée |
| date | TEXT | Date de la prévision |
| temp_max | REAL | Température maximale |
| temp_min | REAL | Température minimale |
| etat | TEXT | Condition météo avec emoji |
| ville | TEXT | Nom de la ville |

---

## Améliorations Futures

- Ajout de la géolocalisation automatique
- Mode sombre/clair
- Support multilingue
- Graphiques de température
- Notifications pour les alertes météo
- Cache des recherches récentes

---


