import requests as rq
import json
import pandas as pd
from pathlib import Path 
import sys

# Get week results from NFL
api_key = 'c06d462a00a745a3845c0e331a30b5f5'
response = rq.get('https://api.sportsdata.io/v3/nfl/scores/json/ScoresByWeek/2022REG/{}?key={}'.format(sys.argv[1], api_key))
games = json.loads(response.text)

# Table for short name of each team
short_to_full_table = {
  'DEN': 'Broncos',
  'BAL': 'Ravens',
  'CAR': 'Panthers',
  'CHI': 'Bears',
  'MIA': 'Dolphins',
  'ARI': 'Cardinals',
  'LV': 'Raiders',
  'NE': 'Patriots',
  'PIT': 'Steelers',
  'TEN': 'Titans',
  'WAS': 'Commanders',
  'SF': '49ers',
  'NYG': 'Giants',
  'GB': 'Packers',
  'CIN': 'Bengals',
  'JAX': 'Jaguars',
  'TB': 'Buccaneers',
  'ATL': 'Falcons',
  'DAL': 'Cowboys',
  'DET': 'Lions',
  'MIN': 'Vikings',
  'NO': 'Saints',
  'NYJ': 'Jets',
  'PHI': 'Eagles',
  'HOU': 'Texans',
  'IND': 'Colts',
  'LAR': 'Rams',
  'SEA': 'Seahawks',
  'BUF': 'Bills',
  'CLE': 'Browns',
  'LAC': 'Chargers',
  'KC': 'Chiefs',
}

# Build the results dict from data
results = {}
for game in enumerate(games) :
  home_team = short_to_full_table[game[1]['HomeTeam']].lower()
  away_team = short_to_full_table[game[1]['AwayTeam']].lower()
  home_score = game[1]['HomeScore']
  away_score = game[1]['AwayScore']

  results[home_team] = {}
  results[home_team]['team_score'] = home_score
  results[home_team]['opp_score'] = away_score
  results[home_team]['w'] = home_score > away_score

  results[away_team] = {}
  results[away_team]['team_score'] = away_score
  results[away_team]['opp_score'] = home_score
  results[away_team]['w'] = home_score < away_score

# Store results for later use
df = pd.DataFrame.from_dict(results, orient='index')
df.head()
filepath = Path('data/results_w{}.csv'.format(sys.argv[1]))  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)