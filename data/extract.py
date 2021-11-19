# imports

import tweepy as tw
from utils import utils
from datetime import datetime

AUTH_DATA = utils.load_json('auth.json')

auth = tw.OAuthHandler(AUTH_DATA['consumer_key'], AUTH_DATA['consumer_secret'])
auth.set_access_token(AUTH_DATA['access_token'], AUTH_DATA['access_secret'])

def add_busca(obj, termo):
    # print(type(obj))
    obj['busca'] = termo
    return obj

querys = [
    '(desmatamento OR desflorestamento)',
    '(chuva AND forte)',
    '(mudança AND climatica)',
    '(queimada OR seca)'
    'alagamento',
    '(vento AND forte)',
    '(desmatamento AND amazonia)',
    '(pantanal AND amazonia)',
    'seca'
    'temporal'
    ]
date_since = '2021-01-01'

for search_words in querys:
    print(f'[BUSCA]{search_words}')
    api = tw.API(auth=auth, wait_on_rate_limit=True)
    tweets = tw.Cursor(
        api.search_tweets, 
        q=search_words, 
        lang="pt-br", 
        since_id=date_since, 
        ).items()
    data = map(lambda x: add_busca(obj=x._json, termo=search_words), tweets)
    utils.to_json(data=[*data], output=f'json/{datetime.now()}.json')
    print(f'[BUSCA]{search_words} - OK')
