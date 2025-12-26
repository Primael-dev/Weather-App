import sqlite3

# Fonction qui sauvegarde les données météo dans la base de données
def save(datas):
    conn = None
    try:
        # Connexion à la base de données SQLite
        conn = sqlite3.connect("weather.db")
        cursor = conn.cursor()

        # Création de la table si elle n'existe pas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS previsions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                temp_max REAL,
                temp_min REAL,
                etat TEXT,
                ville TEXT
            )
        ''')

        # Insertion de chaque jour dans la base de données
        for day in datas:
            cursor.execute('''
                INSERT INTO previsions (date, temp_max, temp_min, etat, ville)
                VALUES (?, ?, ?, ?, ?)
            ''', (day['date'], day['max'], day['min'], day['state'], day['city']))

        # Validation des changements
        conn.commit()
        return True
    except (sqlite3.OperationalError, sqlite3.IntegrityError, Exception) as e:
        print(f"error: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print("Bdd close")

# Fonction qui récupère toutes les prévisions de la base de données
def get_all():
    conn = None
    try:
        # Connexion à la base de données
        conn = sqlite3.connect("weather.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Sélection de toutes les prévisions
        cursor.execute("SELECT * FROM previsions")
        
        # Conversion des résultats en liste de dictionnaires
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"error: {e}")
        return []
    finally:
        if conn:
            conn.close()