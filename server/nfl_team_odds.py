import requests
import json
import pandas as pd

# Load config
with open('json/config.json') as f:
    config = json.load(f)

# Global variables
url = config['API']['nfl_team_odds_url']
params = {
    "apiKey": config['API']['api_key'],
    "regions": config['API']['region'],
}

def get_team_markets():
    '''
    Uses the Odds API to create a request that returns the team market betting data.
    It takes that data and then filters it down into a data frame with only
    the data from FanDuel.

    :return pd.DataFrame: data frame with fanduel odds
    '''

    # Create reponse and store data
    response = requests.get(url, params=params)
    if response.status_code == 200:
        nfl_team_markets = response.json() 

    # Filter down to Fanduel data
    nfl_team_odds  = []
    for game in nfl_team_markets:
        for bookmaker in game["bookmakers"]:
            for market in bookmaker["markets"]:
                for outcome in market["outcomes"]:
                    nfl_team_odds.append({
                        'id': game['id'],
                        'sport_key': game['sport_key'],
                        'sport_title': game['sport_title'],
                        'commence_time': game['commence_time'],
                        'home_team': game['home_team'],
                        'away_team': game['away_team'],
                        'bookmaker_key': bookmaker['key'],
                        'bookmaker_title': bookmaker['title'],
                        'bookmaker_last_update': bookmaker['last_update'],
                        'market_key': market['key'],
                        'market_last_update': market['last_update'],
                        'outcome_name': outcome['name'],
                        'outcome_price': outcome['price']
                    })

    # Convert to DataFrame
    nfl_team_odds_df = pd.DataFrame(nfl_team_odds)

    # Consolidate to Fanduel
    nfl_team_fanduel_df = nfl_team_odds_df[nfl_team_odds_df['bookmaker_key'] == 'fanduel']

    return nfl_team_fanduel_df

def clean_dataframe(df: pd.DataFrame):
    '''
    Takes the data frame created by the get_team_markets() method and
    cleans the data types, unnecessary columns and aggregates each event market
    to one singular line

    :param pd.DataFrame nfl_fanduel_odds: df with game odds
    :return pd.DataFrame : cleaned df with game odds
    '''
    
    # Aggregate rows to one row per event
    df['home_price'] = None
    df['away_price'] = None
    
    # Map the prices
    for idx, row in df.iterrows():
        if row['outcome_name'] == row['home_team']:
            df.at[idx, 'home_price'] = row['outcome_price']
        elif row['outcome_name'] == row['away_team']:
            df.at[idx, 'away_price'] = row['outcome_price']

    # Drop unnecessary rows
    df.drop(columns=['sport_key', 'bookmaker_key', 'bookmaker_last_update', 
                     'market_last_update', 'outcome_name', 'outcome_price'], inplace=True)
    
    # Aggregate the missing data and drop duplicates
    df_combined = df.groupby(['id', 'sport_title', 'commence_time', 'home_team', 
                     'away_team', 'bookmaker_title'], as_index=False).agg(
                    {'home_price': 'max','away_price': 'max'})
    
    # Format commence time
    

    return df_combined

# def main():
#     '''
#     Main method that calls the other methods in order to retrieve,
#     clean, and return data frame with the given odds for each
#     NFL event.

#     :return pd.DataFrame: NFL event odds
#     '''

#     # Retrieve market odds from API
#     nfl_fanduel_odds = get_team_markets()

#     # Clean data and format into pandas data frame
#     nfl_fanduel_odds = clean_dataframe(nfl_fanduel_odds)

#     print(nfl_fanduel_odds)

#     return nfl_fanduel_odds

if __name__ == '__main__':
    # Retrieve market odds from API
    nfl_fanduel_odds = get_team_markets()

    # Clean data and format into pandas data frame
    nfl_fanduel_odds = clean_dataframe(nfl_fanduel_odds)

    print(nfl_fanduel_odds)
