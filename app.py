# Importation des modules
import os
from flask import Flask, send_from_directory
from backend.routes import api_bp
from flask_cors import CORS

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# Enregistrement de la blueprint
app.register_blueprint(api_bp)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)