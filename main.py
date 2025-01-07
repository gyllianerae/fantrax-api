from flask import Flask, request, jsonify, redirect, url_for, session
from fantraxapi import FantraxAPI
from requests import Session as RequestsSession
import subprocess
import time
import os
import pickle

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for secure session

# Route: Home - Trigger `login.py` and redirect user to complete login
@app.route('/')
def index():
    if 'cookies' in session:
        return redirect(url_for('fetch_league_details'))  # If cookies exist, fetch league data
    return redirect(url_for('start_login'))

# Route: Trigger `login.py` and redirect to complete login
@app.route('/start_login', methods=['GET'])
def start_login():
    try:
        # Run `login.py` to open Fantrax login window
        subprocess.Popen(["python", "login.py"])  # Run login.py in the background
        time.sleep(5)  # Wait briefly for login to open
        return '''
            <h2>Fantrax Login</h2>
            <p>Please log in to Fantrax in the browser window that opened.</p>
            <p>Once logged in, <a href="/callback">click here</a> to confirm login and continue.</p>
        '''
    except Exception as e:
        return f"<h3>Error: {e}</h3>"

# Route: Callback after login - Capture cookies from `login.py`
@app.route('/callback', methods=['GET'])
def callback():
    try:
        # Instead of reading from a file, simulate fetching cookies from `login.py`
        with open("fantraxloggedin.cookie", "rb") as f:
            cookies = pickle.load(f)

        # Save cookies in Flask session (stored in the browser)
        session['cookies'] = cookies
        return '''
            <h2>Login Successful!</h2>
            <p>Cookies have been stored. You can now access your Fantrax data:</p>
            <p><a href="/fetch_league_details">Fetch League Details</a></p>
        '''
    except Exception as e:
        return f"<h3>Error capturing cookies: {e}</h3>"

# Route: Fetch all league details using browser-stored cookies
@app.route('/fetch_league_details', methods=['GET'])
def fetch_league_details():
    if 'cookies' not in session:
        return "<h3>Error: No login session found. Please log in first.</h3>"

    # Load cookies from Flask session
    cookies = session.get('cookies')
    api_session = RequestsSession()
    for cookie in cookies:
        api_session.cookies.set(cookie["name"], cookie["value"])

    # Initialize Fantrax API session
    api = FantraxAPI(league_id="dszhdnrhm5h6iic2", session=api_session)

    try:
        league_data = {}
        print("Fetching all available league data...\n")

        # Fetch standings
        standings = api.standings()
        league_data["standings"] = {}

        if hasattr(standings, 'ranks') and isinstance(standings.ranks, dict):
            for rank, record_obj in standings.ranks.items():
                # Convert the `Record` object to a dictionary
                record_data = {
                    "team_name": record_obj.team.name if hasattr(record_obj, "team") else "Unknown",
                    "wins": getattr(record_obj, "wins", 0),
                    "losses": getattr(record_obj, "losses", 0),
                    "ties": getattr(record_obj, "ties", 0),
                    "points_for": getattr(record_obj, "points_for", 0),
                    "points_against": getattr(record_obj, "points_against", 0),
                }
                league_data["standings"][rank] = record_data

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

            # Convert roster object to JSON-friendly format
            roster_data = {
                "players": [player.name for player in getattr(roster, "players", [])],
                "positions": getattr(roster, "positions", {}),
            }
            rosters[team_name] = roster_data

        league_data["rosters"] = rosters

        # Fetch the trade block
        league_data["trade_block"] = api.trade_block() or "No trade block available"

        # Fetch transactions
        league_data["transactions"] = api.transactions() or "No transactions available"

        # Fetch playoff information
        league_data["playoffs"] = api.playoffs() or "No playoff information available"

        # Fetch pending trades
        league_data["pending_trades"] = api.pending_trades() or "No pending trades available"

        # Fetch positions
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

# Route: Logout and clear cookies
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('cookies', None)  # Remove cookies from session
    return '''
        <h2>Logged Out</h2>
        <p>Your session has been cleared. <a href="/">Login again</a>.</p>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
