from flask import Flask, jsonify
from fantraxapi import FantraxAPI
from requests import Session
import pickle

def load_cookies(cookie_file):
    session = Session()
    try:
        with open(cookie_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                session.cookies.set(cookie["name"], cookie["value"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Cookie file '{cookie_file}' not found.")
    return session

app = Flask(__name__)

last_year = "8wv0vq3im5htwn2z"
this_year = "yae6qgmoljsmydnu"
cookie_file = "fantraxloggedin.cookie"

try:
    session = load_cookies(cookie_file)
    api = FantraxAPI(last_year, session=session)
except Exception as e:
    print(f"Error: {e}")
    exit("Initialization failed.")

@app.route('/teams', methods=['GET'])
def get_teams():
    try:
        teams = [team.name for team in api.teams]
        return jsonify(teams)
    except Exception as e:
        print(f"Error fetching teams: {e}")
        return jsonify({"error": "Unable to fetch teams", "details": str(e)}), 500

@app.route('/league', methods=['GET'])
def get_league():
    try:
        league = {
            "name": api.league.name,
            "sport": api.league.sport,
            "scoring_type": api.league.scoring_type
        }
        return jsonify(league)
    except Exception as e:
        print(f"Error fetching league data: {e}")
        return jsonify({"error": "Unable to fetch league data", "details": str(e)}), 500

@app.route('/players', methods=['GET'])
def get_players():
    try:
        players = [{"name": player.name, "team": player.team.name} for player in api.players]
        return jsonify(players)
    except Exception as e:
        print(f"Error fetching players: {e}")
        return jsonify({"error": "Unable to fetch players", "details": str(e)}), 500

@app.route('/')
def index():
    return jsonify({
        "status": "Fantrax API is running!",
        "version": "1.0.0",
        "available_routes": ["/teams", "/league", "/players"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
