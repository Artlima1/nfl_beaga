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
comment_id = comments[0]['id']
response = rq.get('https://graph.facebook.com/v15.0/{}?fields=text,username&access_token={}'.format(comment_id, access_token))
data = json.loads(response.text)

# Set the bets dict
bets = {}
for comment in comments:
  username = comment['username']
  user_bets = comment['text'].split()
  bets[username] = {}
  bets[username]['spread-lock'] = user_bets[0]
  bets[username]['spread-normal'] = user_bets[1]
  bets[username]['h2h-lock'] = user_bets[2]
  bets[username]['h2h-normal'] = user_bets[3]
  bets[username]['over'] = user_bets[4]
  bets[username]['under'] = user_bets[5]
  bets[username]['upset'] = user_bets[6]

# Store data
df = pd.DataFrame.from_dict(bets, orient='index')
filepath = Path('data/bets_w{}.csv'.format(sys.argv[2]))  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)