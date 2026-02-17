import hashlib
import time
import os
import requests
import sys
import json
import feedparser
from spotify_utils import get_latest_user_episodes

from dotenv import load_dotenv
load_dotenv('.secrets', interpolate=False)

class InvalidRequestError(Exception):
    pass
class EmptyResposeError(Exception):
    pass



#Extracting env vars
api_key = os.getenv('PODCAST_INDEXING_KEY')
api_secret = os.getenv('PODCAST_INDEXING_SECRET')

def get_auth_headers():
    epoch_time = int(time.time())
    data_to_hash = api_key + api_secret + str(epoch_time)
    hashed_string = hashlib.sha1(data_to_hash.encode()).hexdigest()

    return {
        'X-Auth-Date': str(epoch_time),
        'X-Auth-Key': api_key,
        'Authorization': hashed_string,
        'User-Agent': 'PodLearn/1.0'
    }


def get_shows_feed(show_name):

    url = "https://api.podcastindex.org/api/1.0/search/byterm?q=" + show_name
    respose = requests.post(url=url, headers=get_auth_headers())

    if respose.status_code != 200:
        print ('<< Received ' + str(respose.status_code) + '>>')
        raise InvalidRequestError
    
    respose_data = respose.json()

    if len(respose_data.get('feeds')) <= 0:
        raise EmptyResposeError

    shows = []
    for show in respose_data['feeds']:
        result = {
            'id' : show['id'],
            'title' : show['title'],
            'url' : show['url'],
            'categories' : show['categories'],
        }
        shows.append(result)

    return shows


def get_episodes(show):
    parser = feedparser.parse(show['url'])
    episodes = []
    for entry in parser.entries:
        if entry.itunes_duration < 300:
            print(entry.enclosures[0]['href'])
            result = {
                'title' : entry.title,
                'season': entry.itunes_season,
                'episode_num': entry.itunes_episode,
                'duration': entry.itunes_duration,
                'audio_href': entry.enclosures[0]['href'],
            }

def get_filtered_episodes():
    a= 0
    #if spotfy_episode['name'] == podindex_episode['title']
    #if spotfy_episode['show_name'] == podindex_show['title']
    #if spotfy_episode['duration'] is around podindex_show['duration']
    #then add podindex_episode to final*_episodes


if __name__ == "__main__":
    #Getting console arguments
    # parser = argparse.ArgumentParser()
    # parser.add_argument(dest='search_query', type=str, help="Query to search podcastindex.org for")

    

    #print(get_latest_user_episodes()[0])


    shows = get_shows_feed(sys.argv[1])
    print(s['url'] for s in shows)
    #get_episodes(show)