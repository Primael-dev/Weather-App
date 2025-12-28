#importation des modules
import pytest
import sqlite3
import os
from flask import json
from app import app
from database import saver
from core.cleaner import cleaner

# configuration de pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    test_db_path = "test_weather_temp.db"
    
    # On sauvegarde la fonction originale
    original_connect = sqlite3.connect

    # On mock pour diriger vers le fichier de test
    def mock_connect(*args, **kwargs):
        return original_connect(test_db_path)
    
    saver.sqlite3.connect = mock_connect

    # Initialisation de la table dans la base de test
    conn = original_connect(test_db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS previsions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, temp_max REAL, temp_min REAL, etat TEXT, ville TEXT
        )
    ''')
    conn.commit()
    conn.close()

    with app.test_client() as client:
        yield client

    # Nettoyage après les tests : on remet l'original et on supprime le fichier
    saver.sqlite3.connect = original_connect
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

# tests

# Test de la fonction cleaner
def test_cleaner_transformation():
    raw_data = {
        'daily': {
            'time': ['2025-12-25'],
            'temperature_2m_max': [32.5],
            'temperature_2m_min': [24.0],
            'weathercode': [0]
        }
    }
    result = cleaner(raw_data, "Cotonou")
    assert result[0]['city'] == "Cotonou"
    assert result[0]['state'] == "Ciel dégagé ☀️"

# Tests de l'API
def test_get_weather_empty(client):
    response = client.get('/api/weather')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'

# Tests de l'API
def test_post_weather_success(client):
    # Ce test appelle la vraie API Open-Meteo
    payload = {"city": "Cotonou"}
    response = client.post('/api/weather', 
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 201

# Tests de la base de données
def test_database_persistence(client):
    test_data = [{
        'date': '2025-12-27',
        'max': 30.0,
        'min': 20.0,
        'state': 'Pluie 🌧️',
        'city': 'Ouidah'
    }]
    
    # Sauvegarde
    save_status = saver.save(test_data)
    assert save_status is True
    
    # Lecture
    db_data = saver.get_all()
    assert len(db_data) > 0
    assert db_data[0]['ville'] == "Ouidah"