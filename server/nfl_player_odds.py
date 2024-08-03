import requests
import json
import pandas as pd
import nfl_team_odds

# Load config
with open('json/config.json') as f:
    config = json.load(f)

# Global variables
url_prexix = config['API']['nfl_player_odds_prefix']
url_suffix = config['API']['nfl_player_odds_suffix']
params = {
    "apiKey": config['API']['api_key'],
    "regions": config['API']['region'],
}

def get_player_markets():

    # Retrieve team odds for event ids
    nfl_team_odds_df = nfl_team_odds.main()

    for event_id in nfl_team_odds_df['id'].unique():
        
        # Create unique url for each event
        url =  f'{url_prexix}/{event_id}/{url_suffix}'

        # Create reponse and store data
        response = requests.get(url, params=params)
        if response.status_code == 200:
            nfl_player_markets = response.json()
        else:
            print('Failed.')

        # Dump the retrieved data into a JSON file
        file_path = f'json/nfl_player_markets_{event_id}.json'
        with open(file_path, 'w') as json_file:
            json.dump(nfl_player_markets, json_file, indent=4)


if __name__ == "__main__":
    get_player_markets()
