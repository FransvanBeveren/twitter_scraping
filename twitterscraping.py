import os

# !!!!BELANGRIJK!!!! 
# Je kan hier je het aantal maximale resultaten bepalen, 50 is bijvoorbeeld --max-results 50
# wil je alles, haal dan --max-results 20 gewoon weg
# Voer tussen \"  \" je zoekfunctie in, voor meer search-operators zie https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators
# Probeer deze zoekopdracht eerst even uit op twitter zelf, dan weet je zeker dat je de juiste tweet scraped
# Ik gebruik lang:nl om alleen in het Nederlands te zoeken en -from:GoThorium om alles van de user @GoThorium te negeren
# Vervang tweets.json voor de naam die jij het bestand wil geven, vergeet niet .json erachter te laten staan
# Voor meer info over deze functie en om hem aan te passen zie: https://github.com/JustAnotherArchivist/snscrape 
# Meer informatie over de functies van SNScrape: https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af
os.system("snscrape --jsonl --progress twitter-search \"(thorium OR thoriumcentrale) lang:nl -from:GoThorium\" > tweets.json")

# Importing pandas

import pandas as pd
from pandas.io.json import json_normalize
import warnings
warnings.filterwarnings("ignore")

# Read JSON file created above
# !!!!BELANGRIJK!!!! Vervang tweets.json voor de naam die je hierboven hebt gebruikt
raw_tweets = pd.read_json(r'tweets.json', lines=True)

# Normalizing the fields and creating DataFrames

users = json_normalize(raw_tweets['user'])
users.drop(['description', 'linkTcourl'], axis=1, inplace=True)
users.rename(columns={'id':'userId', 'url':'profileUrl'}, inplace=True)
users = pd.DataFrame(users)
user_id = []
for user in raw_tweets['user']:
    uid = user['id']
    user_id.append(uid)
raw_tweets['userId'] = user_id

# Cleaning up columns
cols = ['url', 'date', 'renderedContent', 'id', 'userId', 'replyCount', 'retweetCount', 'likeCount', 'quoteCount', 'source', 'media', 'retweetedTweet', 'quotedTweet', 'mentionedUsers']
tweets = raw_tweets[cols]
tweets.rename(columns={'id':'tweetId', 'url':'tweetUrl'}, inplace=True)

# Convert to DataFrame and printing to csv
tweets = pd.DataFrame(tweets)
tweets.drop_duplicates(subset=['tweetId'], inplace=True)

#!!!!BELANGRIJK!!!! Vervang tweets.csv voor de naam die jij het .csv bestand wil geven, vergeet niet .csv erachter te laten staan
tweets.to_csv(r'tweets.csv', encoding='utf-8')

# Voor meer info over wat ik hier gebruikt heb en hoe je het kan aanpassen, zie https://www.kaggle.com/prathamsharma123/clean-raw-json-tweets-data