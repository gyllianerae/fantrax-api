from flask import Flask, jsonify
from fantraxapi import FantraxAPI

app = Flask(__name__)

@app.route("/")
def get_teams():
    last_year = "96idm2rtl8mjk7ol"
    api = FantraxAPI(last_year)
    teams = [team.name for team in api.teams]
    return jsonify(teams)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
