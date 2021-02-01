# Import the Twython class
from twython import Twython
import json
import pandas as pd
import sys

screen_name = F"paulgrossinger"

# Load credentials from json file and instantiate object
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

def get_follower_count(tw, screen_name):
    return tw.show_user(screen_name=screen_name)['followers_count']

def get_tweets(tw, screen_name):
    # get tweets
    user_timeline = None
    try:
       user_timeline = tw.get_user_timeline(screen_name=screen_name)
    except Exception as e:
       print (e)
    return pd.DataFrame(user_timeline, columns=['created_at', 'text', 'retweeted', 'retweet_count'])

# This only gets the first 100 followers, we need to follow cursors to get the rest
def get_followers(tw, screen_name):
    # Get followers
    fl = tw.get_followers_list(screen_name=screen_name)
    return pd.DataFrame(fl['users'], columns=['id', 'name', 'screen_name', 'description'])

def search_query(tw):
    # Create our query
    query = {'q': 'learn python',
        'result_type': 'popular',
        'count': 10,
        'lang': 'en',
        }

    # Search tweets
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
    for status in tw.search(**query)['statuses']:
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['text'])
        dict_['favorite_count'].append(status['favorite_count'])

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)
    df.sort_values(by='favorite_count', inplace=True, ascending=False)
    return df

if __name__ == '__main__':

    tweets_df = get_tweets(python_tweets, screen_name)
    print (tweets_df)

    followers_df = get_followers(python_tweets, screen_name)
    print (followers_df)

    print (F"Follower count: {get_follower_count(python_tweets, screen_name)}")

    
