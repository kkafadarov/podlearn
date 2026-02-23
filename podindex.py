import hashlib
import time
import os
import requests
import feedparser
from fuzzywuzzy import fuzz
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

def parse_duration(duration_str):
    parts = str(duration_str).split(':')
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1])*60 + int(parts[2])
    if len(parts) == 2:
        return int(parts[0])*60 + int(parts[1])
    if len(parts) == 1:
        return int(parts[0])

    return None

def get_episodes(show):
    parser = feedparser.parse(show['url'])
    episodes = []
    for entry in parser.entries:
        if not hasattr(entry, 'itunes_duration'):
            continue

        ep_duration = parse_duration(entry.itunes_duration)
        if ep_duration > 300:
            result = {
                'title' : entry.title,
                #'pubDate': entry.pubDate,
                #'episode_num': entry.itunes_episode,
                'duration': ep_duration,
                'audio_href': entry.enclosures[0]['href'],
            }
            episodes.append(result)
    return episodes

def same(podid_episode, spotfy_episode):
    title_similarity = fuzz.ratio(
        podid_episode['title'].lower(),
        spotfy_episode['name'].lower()
    )

    duration_diff = abs(
        int(podid_episode['duration']) - int(spotfy_episode['duration_ms']) * 0.001
    )

    if title_similarity > 85:
        return True

    if title_similarity > 60 and duration_diff < 30:
        return True

    return False

def match_episodes(spotfy_episodes):
    matched = {}
    for sp_show, sp_episodes in spotfy_episodes.items():
        try:
            show_feed = get_shows_feed(sp_show)
        except EmptyResposeError:
            print("Show not found")
            continue

        podid_episodes = (get_episodes(show_feed[0]))
        
        result = []
        for sep in sp_episodes:
            for pep in podid_episodes:
                if same(pep, sep):
                    result.append(pep)
                    break

        if result:
            matched[sp_show] = result

    return matched


if __name__ == "__main__":
    sp_latest_episodes = get_latest_user_episodes()
    episodes_to_downwload = match_episodes(sp_latest_episodes)