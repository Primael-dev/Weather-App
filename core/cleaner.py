from core.getLocation import get_ville

# Fonction qui convertit un code météo en description lisible avec emoji
def clean_map(code):
    dico = {
        0: "Ciel dégagé ☀️",
        1: "Principalement dégagé 🌤️",
        2: "Partiellement nuageux ⛅",
        3: "Couvert ☁️",
        45: "Brouillard 🌫️",
        48: "Brouillard givrant 🌫️",
        51: "Bruine légère 🌧️",
        53: "Bruine modérée 🌧️",
        55: "Bruine dense 🌧️",
        61: "Pluie légère 🌦️",
        63: "Pluie modérée 🌧️",
        65: "Pluie forte 🌧️",
        71: "Neige légère ❄️",
        73: "Neige modérée ❄️",
        75: "Neige forte ❄️",
        77: "Grains de neige ❄️",
        80: "Averses de pluie légères 🌦️",
        81: "Averses de pluie modérées 🌧️",
        82: "Averses de pluie violentes ⛈️",
        85: "Averses de neige légères 🌨️",
        86: "Averses de neige fortes 🌨️",
        95: "Orage ⚡",
        96: "Orage avec grêle légère ⛈️",
        99: "Orage avec grêle forte ⛈️"
    }
    return dico.get(code, f"Code {code} inconnu")

# Fonction qui nettoie et formate les données brutes de l'API météo
def cleaner(raw_data,city_name):

    try:
    
        # Liste qui contiendra les données formatées de chaque jour
        list_final = []

        # Extrait les informations quotidiennes
        daily_info = raw_data.get('daily', {})
        
        # Compte le nombre de jours disponibles
        days = len(daily_info.get('time', []))

        # Parcourt chaque jour pour créer une fiche météo
        for i in range(days):
            
            # Crée un dictionnaire avec les infos du jour
            fiche_du_jour = {
                "date": daily_info['time'][i],
                "max": float(daily_info['temperature_2m_max'][i]),
                "min": float(daily_info['temperature_2m_min'][i]),
                "state": clean_map(daily_info['weathercode'][i]),
                "city": city_name
            }
            list_final.append(fiche_du_jour)
            
        return list_final
    
    except Exception as e:
        print(f"Error during the cleaning :{e}")
        return