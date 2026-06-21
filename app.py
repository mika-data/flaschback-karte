from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__, template_folder='templates')

OSM_FILE = 'data_osm.json'
ITEMS_FILE = 'items.json'

# Initiale Struktur absichern
if not os.path.exists(ITEMS_FILE):
    with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

if not os.path.exists(OSM_FILE):
    with open(OSM_FILE, 'w', encoding='utf-8') as f:
        # Ein leeres Fallback-Array schreiben
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

# Endpunkt für das OSM-Gebäude-Gelände (GET)
@app.route('/api/osm', methods=['GET'])
def get_osm_data():
    try:
        with open(OSM_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpunkt für das interaktive CMS (GET zum Laden, POST zum Speichern)
@app.route('/api/items', methods=['GET', 'POST'])
def handle_items_cms():
    if request.method == 'POST':
        try:
            items_data = request.json
            with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
                json.dump(items_data, f, indent=4, ensure_ascii=False)
            return jsonify({"status": "success", "message": "Layout permanent in items.json gesichert."})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        try:
            with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        except Exception as e:
            return jsonify([])

if __name__ == '__main__':
    # Startet auf Port 5000 (für externe Zugriffe '0.0.0.0' nutzen)
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')

