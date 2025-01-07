import pickle
from fantraxapi import FantraxAPI
from requests import Session

# Initialize a session
session = Session()

# Load cookies into the session
with open("fantraxloggedin.cookie", "rb") as f:
    for cookie in pickle.load(f):
        session.cookies.set(cookie["name"], cookie["value"])

# Specify the League ID
league_id = "96igs4677sgjk7ol"

# Create an API instance
api = FantraxAPI(league_id, session=session)

# Test an authenticated request
try:
    print(api.teams())
except Exception as e:
    print(f"Error details: {e}")