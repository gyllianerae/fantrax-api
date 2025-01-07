from flask import Flask, jsonify
from fantraxapi import FantraxAPI
from requests import Session
import pickle

# Load session cookies from the cookie file
def load_cookies(cookie_file):
    session = Session()
    try:
        with open(cookie_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                session.cookies.set(cookie["name"], cookie["value"])
    except FileNotFoundError:
        print(f"Cookie file '{cookie_file}' not found. Please generate it first.")
        exit()
    return session

# Initialize Flask app
app = Flask(__name__)

# Replace these IDs with your actual league IDs
last_year = "8wv0vq3im5htwn2z"
this_year = "yae6qgmoljsmydnu"

# Load cookies and create a session
cookie_file = "fantraxloggedin.cookie"  # Replace with your cookie file path
session = load_cookies(cookie_file)

# Initialize Fantrax API with session
api = FantraxAPI(last_year, session=session)

# Define a route for teams
@app.route('/teams', methods=['GET'])
def get_teams():
    try:
        teams = [team.name for team in api.teams]
        return jsonify(teams)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define a route for league data
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
        return jsonify({"error": str(e)}), 500

# Define a route for players
@app.route('/players', methods=['GET'])
def get_players():
    try:
        players = [{"name": player.name, "team": player.team.name} for player in api.players]
        return jsonify(players)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define a default route
@app.route('/')
def index():
    return "Fantrax API is running!"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
