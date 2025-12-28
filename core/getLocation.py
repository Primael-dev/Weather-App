import geocoder

# Fonction qui récupère les coordonnées géographiques de l'utilisateur via son IP
def locate():
    try:

        g = geocoder.ip('me')
        
        if g.ok:
            return g.latlng
        return [9.3077, 2.3158] 
    except Exception as e:
            print (f"Error:{e}")
            return [9.3077, 2.3158]

# Fonction qui récupère le nom de la ville de l'utilisateur via son IP    
def get_ville():

    try:
        g = geocoder.ip('me')
        ma_ville = g.city if g.city else "Inconnue"
        return ma_ville
    except Exception as e:
        print (f"Error:{e}")
        return
    

import requests

# Fonction qui récupère les coordonnées d'une ville à partir de son nom
def get_coords_from_city(city_name):
    try:
        # Appel à l'API Nominatim d'OpenStreetMap
        url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
        headers = {'User-Agent': 'Projet6_Weather_App'} 
        
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        # Si des résultats sont trouvés, retourne les coordonnées
        if data:
            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"])
            }
        return None
    except Exception as e:
        print(f"Erreur géocodage : {e}")
        return None