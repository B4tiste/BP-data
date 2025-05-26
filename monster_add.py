import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
json_file = "monster_dates.json"

def load_monster_dates():
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            return json.load(f)
    return {}

def save_monster_dates(monster_dates):
    with open(json_file, "w") as f:
        json.dump(monster_dates, f, indent=4)

@app.route('/')
def index():
    monster_dates = load_monster_dates()
    monster_names = list(monster_dates.keys())
    return render_template("index.html", monster_names=monster_names)

@app.route('/add', methods=["POST"])
def add_monster():
    data = request.json
    monster_name = data.get("monster_name", "")
    date = data.get("date", "")
    if not monster_name or not date:
        return jsonify({"success": False, "message": "Données manquantes."})
    monster_dates = load_monster_dates()
    if monster_name in monster_dates:
        monster_dates[monster_name].append(date)
    else:
        monster_dates[monster_name] = [date]
    save_monster_dates(monster_dates)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
