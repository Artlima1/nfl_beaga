import requests as rq
import json
import pandas as pd
from pathlib import Path
import sys

api_key = 'a89d34dd107d096cf662e99eab2e29ee'

response = rq.get('https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey={}&bookmakers=fanduel&markets=totals,spreads&oddsFormat=american'.format(api_key))
data = json.loads(response.text)

markets = {}

for odds in enumerate(data):
  team = odds[1]['home_team'].split()
  team = team[len(team)-1]
  for market in enumerate(odds[1]['bookmakers'][0]['markets']):
    if market[1]['key'] == 'spreads':
      if market[1]['outcomes'][0]['name'].split()[1] == team :
        spread = market[1]['outcomes'][0]['point']
      else:
        spread = market[1]['outcomes'][1]['point']
    if market[1]['key'] == 'totals':
      ou = market[1]['outcomes'][0]['point']

  markets[team] = {}
  markets[team]['spread'] = spread
  markets[team]['o/u'] = ou

  team = odds[1]['away_team'].split()
  team = team[len(team)-1]
  for market in enumerate(odds[1]['bookmakers'][0]['markets']):
    if market[1]['key'] == 'spreads':
      if market[1]['outcomes'][0]['name'].split()[1] == team :
        spread = market[1]['outcomes'][0]['point']
      else:
        spread = market[1]['outcomes'][1]['point']
    if market[1]['key'] == 'totals':
      ou = market[1]['outcomes'][0]['point']

  markets[team] = {}
  markets[team]['spread'] = spread
  markets[team]['o/u'] = ou

df = pd.DataFrame.from_dict(markets, orient='index')
filepath = Path('data/odds_w{}.csv'.format(shortcode = sys.argv[2]))  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)