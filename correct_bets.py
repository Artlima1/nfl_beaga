import pandas as pd
from pathlib import Path 
import sys

# Load Data
df = pd.DataFrame()
df = pd.read_csv('data/bets_w{}.csv'.format(sys.argv[1]))
df = df.rename(columns={"Unnamed: 0": "bettor"})
df = df.set_index('bettor')
bets = df.to_dict(orient='index')

df = pd.read_csv('data/odds_w{}.csv'.format(sys.argv[1]))
df = df.rename(columns={"Unnamed: 0": "market"})
df = df.set_index('market')
markets = df.to_dict(orient='index')

df = pd.read_csv('data/odds_w{}.csv'.format(sys.argv[1]))
df = df.rename(columns={"Unnamed: 0": "team"})
df = df.set_index('team')
results = df.to_dict(orient='index')

#Correct data
for bettor in bets:
  
  bets[bettor]['result'] = 0

  # spread lock
  team = bets[bettor]['spread-lock']
  result = results[team]['team_score'] - results[team]['opp_score']
  market = markets[team]['spread']
  if (-result) > market :
    bets[bettor]['result'] -= 1
    bets[bettor]['spread-lock'] = False
  else:
    bets[bettor]['spread-lock'] = True

  # spread normal
  team = bets[bettor]['spread-normal']
  result = results[team]['team_score'] - results[team]['opp_score']
  market = markets[team]['spread']
  if -(result) < market:
    bets[bettor]['result'] += 2
    bets[bettor]['spread-normal'] = True
  else :
    bets[bettor]['spread-normal'] = False

  # h2h lock
  team = bets[bettor]['h2h-lock']
  result = results[team]['w']
  if result == False :
    bets[bettor]['result'] -= 2
    bets[bettor]['h2h-lock'] = False
  else :
    bets[bettor]['h2h-lock'] = True

  # h2h normal
  team = bets[bettor]['h2h-normal']
  result = results[team]['w']
  if result == True :
    bets[bettor]['result'] += 1
    team = bets[bettor]['h2h-normal'] = True
  else :
    team = bets[bettor]['h2h-normal'] = False

  # over
  team = bets[bettor]['over']
  result = results[team]['team_score'] + results[team]['opp_score']
  market = markets[team]['o/u']
  if result > market :
    bets[bettor]['result'] += 1
    bets[bettor]['over'] = True
  else :
    bets[bettor]['over'] = False

  # under
  team = bets[bettor]['under']
  result = results[team]['team_score'] + results[team]['opp_score']
  market = markets[team]['o/u']
  if result < market :
    bets[bettor]['result'] += 1
    team = bets[bettor]['under'] = True
  else:
    team = bets[bettor]['under'] = False

  # upset
  team = bets[bettor]['upset']
  result = results[team]['w']
  market = markets[team]['spread']
  if result == True :
    if market > 7.5 :  
      bets[bettor]['result'] += 3
    elif market > 4.5 :
      bets[bettor]['result'] += 2
    bets[bettor]['upset'] = True
  else:
    bets[bettor]['upset'] = False

# Print Weekly Results
ordered_scores = dict(sorted(bets.items(), key = lambda bettor: bettor[1]["result"], reverse=True))
for bettor in ordered_scores:
  print(bettor, ordered_scores[bettor]['result'])

df = pd.DataFrame.from_dict(ordered_scores, orient='index')
filepath = Path('data/scores_w{}.csv'.format(sys.argv[1]))  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)