from flask import Flask, jsonify
from fantrax_wrapper import get_fantrax_api
from fantraxapi import FantraxAPI
from requests import Session
import pickle

# Flask app initialization
app = Flask(__name__)

# League ID and cookie file setup
last_year = "8wv0vq3im5htwn2z"
this_year = "dszhdnrhm5h6iic2"  # Update with your league ID if needed
cookie_file = "fantraxloggedin.cookie"

# Load session cookies
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

# Load API session
try:
    session = load_cookies(cookie_file)
    api = FantraxAPI(this_year, session=session)
except Exception as e:
    print(f"Error: {e}")
    exit("Initialization failed.")

# Route: Home
@app.route('/')
def index():
    return jsonify({
        "status": "Fantrax API is running!",
        "version": "1.0.0",
        "available_routes": ["/teams", "/league", "/players", "/fetch_league_details"]
    })

# Route: Fetch all teams
@app.route('/teams', methods=['GET'])
def get_teams():
    try:
        teams = [team.name for team in api.teams]
        return jsonify(teams)
    except Exception as e:
        print(f"Error fetching teams: {e}")
        return jsonify({"error": "Unable to fetch teams", "details": str(e)}), 500

# Route: Fetch league information
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

# Route: Fetch all players
@app.route('/players', methods=['GET'])
def get_players():
    try:
        players = [{"name": player.name, "team": player.team.name} for player in api.players]
        return jsonify(players)
    except Exception as e:
        print(f"Error fetching players: {e}")
        return jsonify({"error": "Unable to fetch players", "details": str(e)}), 500

# Route: Print all league details
@app.route('/fetch_league_details', methods=['GET'])
def fetch_league_details():
    try:
        league_data = {}
        print("Fetching all available league data...\n")

        # Fetch standings
        standings = api.standings()
        league_data["standings"] = standings.ranks if hasattr(standings, 'ranks') else "No standings available"

        # Fetch all teams
        league_teams = api.teams
        team_list = [team.name for team in league_teams]
        league_data["teams"] = team_list

        # Fetch rosters of each team
        rosters = {}
        for team in league_teams:
            team_id = team.team_id
            team_name = team.name
            roster = api.roster_info(team_id)

            # Convert roster object to a JSON-friendly format
            roster_data = {
                "players": [player.name for player in getattr(roster, "players", [])],
                "positions": getattr(roster, "positions", {}),
            }
            rosters[team_name] = roster_data

        league_data["rosters"] = rosters

        # Other league details (trade block, transactions, etc.)
        league_data["trade_block"] = api.trade_block() or "No trade block available"
        league_data["transactions"] = api.transactions() or "No transactions available"
        league_data["playoffs"] = api.playoffs() or "No playoff information available"
        league_data["pending_trades"] = api.pending_trades() or "No pending trades available"

        positions = api.positions
        league_positions = {}
        if isinstance(positions, dict):
            for pos_code, position_obj in positions.items():
                position_name = getattr(position_obj, 'name', 'Unknown Position')
                max_count = getattr(position_obj, 'max_count', 'Unknown Max Count')
                league_positions[position_name] = max_count
        league_data["positions"] = league_positions

        return jsonify(league_data)

    except Exception as e:
        print(f"Error fetching league details: {e}")
        return jsonify({"error": "Unable to fetch league details", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
