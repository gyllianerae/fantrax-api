# fantrax_wrapper.py
import pickle
from fantraxapi import FantraxAPI
from requests import Session

def get_fantrax_api(league_id):
    session = Session()

    # Load the saved login cookie
    with open("fantraxloggedin.cookie", "rb") as f:
        for cookie in pickle.load(f):
            session.cookies.set(cookie["name"], cookie["value"])

    # Initialize Fantrax API with the session
    api = FantraxAPI(league_id, session=session)
    return api
