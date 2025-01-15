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

# Utility function to safely convert values to float
def safe_float(value):
    if value is None or value == '-' or value == '':
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

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
        # Delete old cookies and login status
        if os.path.exists("fantraxloggedin.cookie"):
            os.remove("fantraxloggedin.cookie")
        if os.path.exists("login_status.txt"):
            os.remove("login_status.txt")

        # Run `login.py` to open Fantrax login window
        subprocess.Popen(["python", "login.py"])  # Run login.py in the background

        return '''
            <h2>Fantrax Login</h2>
            <p>Please log in to Fantrax in the browser window that opened.</p>
            <p>Once logged in, <a href="/check_login_status">click here</a> to check login status and continue.</p>
        '''
    except Exception as e:
        return f"<h3>Error: {e}</h3>"

# Route: Check login status
@app.route('/check_login_status', methods=['GET'])
def check_login_status():
    if os.path.exists("login_status.txt"):
        with open("login_status.txt", "r") as f:
            status = f.read().strip()
            if status == "success":
                return redirect(url_for('callback'))
    return '''
        <h3>Login not completed yet. Please wait or <a href="/check_login_status">check again</a>.</h3>
    '''

# Route: Callback after login - Capture cookies from `login.py`
@app.route('/callback', methods=['GET'])
def callback():
    try:
        # Read the saved cookies after successful login
        with open("fantraxloggedin.cookie", "rb") as f:
            cookies = pickle.load(f)

        # Save cookies in Flask session
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

    cookies = session.get('cookies')
    api_session = RequestsSession()
    for cookie in cookies:
        api_session.cookies.set(cookie["name"], cookie["value"])

    api = FantraxAPI(league_id="dszhdnrhm5h6iic2", session=api_session)

    try:
        league_data = {}
        standings = api.standings()
        league_data["standings"] = {}

        if hasattr(standings, 'ranks') and isinstance(standings.ranks, dict):
            for rank, record_obj in standings.ranks.items():
                # Debugging info to ensure data correctness
                print(f"Rank: {rank}, Record Data: {record_obj.__dict__ if hasattr(record_obj, '__dict__') else record_obj}")

                record_data = {
                    "team_name": record_obj.team if hasattr(record_obj, "team") else "Unknown",
                    "wins": safe_float(getattr(record_obj, "win", 0)),
                    "losses": safe_float(getattr(record_obj, "loss", 0)),
                    "ties": safe_float(getattr(record_obj, "tie", 0)),
                    "points": safe_float(getattr(record_obj, "points", 0)),
                    "points_for": safe_float(getattr(record_obj, "points_for", 0)),
                    "points_against": safe_float(getattr(record_obj, "points_against", 0)),
                    "win_percentage": safe_float(getattr(record_obj, "win_percentage", 0)),
                    "games_back": safe_float(getattr(record_obj, "games_back", 0)),
                }
                league_data["standings"][rank] = record_data

        league_teams = api.teams
        team_list = [team.name for team in league_teams]
        league_data["teams"] = team_list

        rosters = {}
        for team in league_teams:
            team_id = team.team_id
            team_name = team.name
            roster = api.roster_info(team_id)
            roster_data = {
                "players": [player.name for player in getattr(roster, "players", [])],
                "positions": {pos: safe_float(value) for pos, value in getattr(roster, "positions", {}).items()},
            }
            rosters[team_name] = roster_data

        league_data["rosters"] = rosters
        league_data["trade_block"] = api.trade_block() or "No trade block available"
        league_data["transactions"] = api.transactions() or "No transactions available"
        league_data["playoffs"] = api.playoffs() or "No playoff information available"
        league_data["pending_trades"] = api.pending_trades() or "No pending trades available"

        positions = api.positions
        league_positions = {}
        if isinstance(positions, dict):
            for pos_code, position_obj in positions.items():
                position_name = getattr(position_obj, 'name', 'Unknown Position')
                max_count = safe_float(getattr(position_obj, 'max_count', 0))
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
