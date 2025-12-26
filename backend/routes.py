from flask import Blueprint, request, jsonify
import requests
from core.getLocation import get_coords_from_city
from core.cleaner import cleaner
from database.saver import save, get_all

api_bp = Blueprint('api', __name__)

# Route GET pour récupérer tous les logs météo
@api_bp.route('/api/weather', methods=['GET'])
def fetch_weather():
    try:
        # Récupère tous les enregistrements de la base de données
        logs = get_all()
        return jsonify({"status": "success", "data": logs}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route POST pour ajouter une nouvelle recherche météo
@api_bp.route('/api/weather', methods=['POST'])
def add_weather():
    try:
        # Récupère les paramètres de la requête
        params = request.json
        city_name = params.get('city')
        lat = params.get('lat')
        lon = params.get('lon')

        # Si les coordonnées sont fournies directement
        if lat and lon:
            final_city = city_name if city_name else "Ma Position"
            coords = {"lat": lat, "lon": lon}

        # Sinon, cherche les coordonnées à partir du nom de la ville
        elif city_name:
            coords = get_coords_from_city(city_name)
            final_city = city_name
            if not coords:
                return jsonify({"status": "error", "message": "Ville introuvable"}), 404
        else:
            return jsonify({"status": "error", "message": "Données manquantes"}), 400

        # Appel à l'API Open-Meteo pour récupérer les données météo
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
        response = requests.get(url, timeout=10)
        
        # Nettoie et formate les données reçues
        clean_data = cleaner(response.json(), final_city)
        
        # Sauvegarde les données dans la base de données
        save(clean_data)
        
        return jsonify({"status": "success", "data": clean_data}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500