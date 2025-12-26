# Importation des modules
from flask import Flask
from backend.routes import api_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Enregistrement de la blueprint
app.register_blueprint(api_bp)

if __name__ == "__main__":


    app.run(debug=True, port=5000)