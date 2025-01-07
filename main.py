from fantrax_wrapper import get_fantrax_api
from fantraxapi import FantraxAPI

def fetch_league_details(league_id):
    api = get_fantrax_api(league_id)

    try:
        print("Fetching all available league data...\n")

        # Fetch standings
        print("\n--- League Standings ---")
        standings = api.standings()
        if isinstance(standings.ranks, dict):
            for rank, team_info in standings.ranks.items():
                print(f"{rank}: {team_info}")
        else:
            print("Standings data not available")

        # Fetch all teams
        print("\n--- League Teams ---")
        league_teams = api.teams  # Access `teams` as an attribute, not a method
        print(f"Teams Data: {league_teams}")

        if isinstance(league_teams, list):
            for team in league_teams:
                if isinstance(team, dict):
                    print(f"Team Name: {team.get('name', 'Unknown')}")
                else:
                    print(f"Team: {team}")

         # Fetch rosters of each team
        print("\n--- Team Rosters ---")
        for team in league_teams:
            team_id = team.team_id  # Access `team_id` directly
            team_name = team.name
            roster = api.roster_info(team_id)  # Pass `team_id` to `roster_info()`
            print(f"Roster for {team_name} (ID: {team_id}): {roster}")

        # Fetch the trade block
        print("\n--- Trade Block ---")
        trade_block = api.trade_block()
        print(trade_block if trade_block else "No trade block available")

        # Fetch transactions
        print("\n--- League Transactions ---")
        transactions = api.transactions()
        print(transactions if transactions else "No transactions available")

        # Fetch playoff information
        print("\n--- Playoff Info ---")
        playoffs = api.playoffs()
        print(playoffs if playoffs else "No playoff information available")

        # Fetch pending trades
        print("\n--- Pending Trades ---")
        pending_trades = api.pending_trades()
        print(pending_trades if pending_trades else "No pending trades available")

        # Fetch positions
        print("\n--- League Positions ---")
        positions = api.positions  # Access as an attribute
        if isinstance(positions, dict):
            for pos_code, position_obj in positions.items():
                position_name = getattr(position_obj, 'name', 'Unknown Position')  # Access `name`
                max_count = getattr(position_obj, 'max_count', 'Unknown Max Count')  # Access `max_count`
                print(f"Position: {position_name} (Code: {pos_code}), Max Count: {max_count}")
        else:
            print("No position information available")

    except Exception as e:
        print(f"Error fetching league details: {e}")

if __name__ == "__main__":
    league_id = "dszhdnrhm5h6iic2"  # Replace with your league ID
    fetch_league_details(league_id)
    app.run(host="0.0.0.0", port=5000, debug=True)
