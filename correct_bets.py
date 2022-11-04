import pandas as pd
import sys

# Load Data
df = pd.read_csv('data/bets_w{}.csv'.format(sys.argv[1]))
df = df.rename(columns={"Unnamed: 0": "bettor"})
df = df.set_index('bettor')
bets = df.to_dict(orient='index')

df = pd.read_csv('data/odds_w{}.csv'.format(sys.argv[1]))
df = df.rename(columns={"Unnamed: 0": "market"})
df = df.set_index('market')
markets = df.to_dict(orient='index')

#TODO
results = {
    'Bengals': {
        'team_score': 13,
        'opp_score': 32,
        'w': False
    },

    'Bills': {
        'team_score': 27,
        'opp_score': 17,
        'w': True
    },

    'Saints': {
        'team_score': 24,
        'opp_score': 0,
        'w': True
    },

    'Vikings': {
        'team_score': 34,
        'opp_score': 26,
        'w': True
    },

    'Niners': {
        'team_score': 31,
        'opp_score': 14,
        'w': False
    },

    'Colts': {
        'team_score': 16,
        'opp_score': 17,
        'w': False
    },

    'Broncos': {
        'team_score': 21,
        'opp_score': 17,
        'w': True
    },

    'Packers': {
        'team_score': 17,
        'opp_score': 27,
        'w': False
    }
}


#Correct data
for bettor in bets:
  
  bets[bettor]['result'] = 0

  # spread lock
  team = bets[bettor]['spread-lock']
  result = results[team]['team_score'] - results[team]['opp_score']
  market = markets[team]['spread']
  if((-result) > market):
    bets[bettor]['result'] -= 1

  # spread normal
  team = bets[bettor]['spread-normal']
  result = results[team]['team_score'] - results[team]['opp_score']
  market = markets[team]['spread']
  if(-(result) < market):
    bets[bettor]['result'] += 2

  # h2h lock
  team = bets[bettor]['h2h-lock']
  result = results[team]['w']
  if result == False :
    bets[bettor]['result'] -= 2

  # h2h normal
  team = bets[bettor]['h2h-normal']
  result = results[team]['w']
  if result == True :
    bets[bettor]['result'] += 1

  # over
  team = bets[bettor]['over']
  result = results[team]['team_score'] + results[team]['opp_score']
  market = markets[team]['o/u']
  if result > market :
    bets[bettor]['result'] += 1

  # under
  team = bets[bettor]['under']
  result = results[team]['team_score'] + results[team]['opp_score']
  market = markets[team]['o/u']
  if result < market :
    bets[bettor]['result'] += 1

  # upset
  team = bets[bettor]['upset']
  result = results[team]['w']
  market = markets[team]['spread']
  if result == True :
    if market > 7.5 :  
      bets[bettor]['result'] += 3
    elif market > 4.5 :
      bets[bettor]['result'] += 2

# Print Weekly Results
ordered = dict(sorted(bets.items(), key = lambda bettor: bettor[1]["result"], reverse=True))
for bettor in ordered:
  print(bettor, ordered[bettor]['result'])