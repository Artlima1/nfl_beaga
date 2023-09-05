import requests as rq
import json
import pandas as pd
from pathlib import Path
import sys

# to get acces token refer to https://developers.facebook.com/docs/marketing-apis/overview/authentication/?locale=pt_BR
access_token = 'EAAQgMFKuVLkBAPg5msteOO63KxZC2gQBoovvMvTCjjrkTZCeEfL4onrZAuqWy2etEzTEfNpyQnE62PkybwzGU4v6iUxvl7T6a6t8OE75OxErZCBf4JV4ZA0XzU1IWa21ZC3oJn396zE2CP7gTVfw4obGDDJg26tgNzWhbVU8SUs1gKGOQTCZAYa'

# Get ID from facebook page
response = rq.get('https://graph.facebook.com/v15.0/me/accounts?access_token={}'.format(access_token))
page_id = json.loads(response.text)['data'][0]['id']

# Get ID from instagram page linked to that facebook page
response = rq.get('https://graph.facebook.com/v15.0/{}?fields=instagram_business_account&access_token={}'.format(page_id, access_token))
ig_id = json.loads(response.text)['instagram_business_account']['id']

# Get Media IDs for each post 
response = rq.get('https://graph.facebook.com/v15.0/{}/media?access_token={}'.format(ig_id, access_token))
media_list = json.loads(response.text)['data']

# Find correct post - Get the shortcode in the link of the post
shortcode = sys.argv[1]
for media in media_list:
  media_id = media['id']
  response = rq.get('https://graph.facebook.com/v15.0/{}?fields=shortcode&access_token={}'.format(media_id, access_token))
  data = json.loads(response.text)
  if(data['shortcode']==shortcode):
    break

# Get comments from post
response = rq.get('https://graph.facebook.com/v15.0/{}/comments?access_token={}'.format(media_id, access_token))
comments = json.loads(response.text)['data']

# Get user from comments
comments_data = [None] * len(comments)

for index, comment in enumerate(comments):
  response = rq.get('https://graph.facebook.com/v15.0/{}?fields=text,username&access_token={}'.format(comment['id'], access_token))
  data = json.loads(response.text)
  new_data = {
      'username': data['username'],
      'text': data['text']
  }
  comments_data[index] = new_data

# Helper vars
teams = [
  'broncos', 'ravens', 'panthers', 'bears',
  'dolphins', 'cardinals', 'raiders', 'patriots',
  'steelers', 'titans', 'commanders', '49ers',
  'giants', 'packers', 'bengals', 'jaguars',
  'buccaneers', 'falcons', 'cowboys', 'lions',
  'vikings', 'saints', 'jets', 'eagles',
  'texans', 'colts', 'rams', 'seahawks',
  'bills', 'browns', 'chargers', 'chiefs',
]

synonims = {
  'bucs' : 'buccaneers',
  'niners': '49ers',
  'pats': 'patriots',
  'cards': 'cardinals',
  'jags': 'jaguars',
}

# Set the bets dict
bets = {}
for comment in comments_data:
  username = comment['username']
  user_bets = comment['text'].replace(",", "")
  user_bets = user_bets.replace(" e", "")
  user_bets = user_bets.lower()
  user_bets = user_bets.split()
  for i in range(0, len(user_bets)):
    if user_bets[i] not in teams:
      user_bets[i] = synonims[user_bets[i]]
  bets[username] = {}
  bets[username]['h2h-lock'] = user_bets[0]
  bets[username]['h2h-normal'] = user_bets[1]
  bets[username]['spread-lock'] = user_bets[2]
  bets[username]['spread-normal'] = user_bets[3]
  bets[username]['over'] = user_bets[4]
  bets[username]['under'] = user_bets[5]
  bets[username]['upset'] = user_bets[6]

# Store data
df = pd.DataFrame.from_dict(bets, orient='index')
print(df)
filepath = Path('data/bets_w{}.csv'.format(sys.argv[2]))  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)