import sys
import os
import requests
from urllib.parse import quote

API_TOKEN = os.getenv('LISTEN_NOTES_TOKEN')
BASE_API_URL = 'https://listen-api.listennotes.com/api/v2'


class EpisodeNotFoundError(Exception):
    pass

def find_podcast_episode(episode_name, show_name):
    params = {
        "q": episode_name,
        "type": "episode",
        "only_in": "title,description",
        "safe_mode": 1,
    }
    headers = {
        'X-ListenAPI-Key': API_TOKEN,
    }

    response = requests.get(url=f'{BASE_API_URL}/search', params=params, headers=headers).json()
    if not response.get("results", None):
        # Encode the query (catch special characters, non-English language, etc) and try again
        params['q'] = quote(episode_name)
        response = requests.get(url=f'{BASE_API_URL}/search', params=params, headers=headers).json()
        if not response.get("results", None):
            # maybe this just doesn't exist.. maybe we need to fix some bugs. give up for now.
            raise EpisodeNotFoundError

    episode_data = response["results"][0]
    # TODO: Double check that show_name matches and raise some exception if it doesn't
    return episode_data


if __name__ == "__main__":
    """ Get a single episode metadata by running `python listen_notes_api 'Episode Name' 'Show Name'`"""
    episode_name = sys.argv[1]
    show_name = sys.argv[2]

    episode_data = find_podcast_episode(episode_name, show_name)

    if episode_data.get("transcript", None):
        print(f'Found a transcript for {show_name}: {episode_name}:\n--------------------------')
        print(episode_data["transcript"])
    else:
        print(f'No a transcript for {show_name}: {episode_name}\n')
        print(f'Generate manually from the audio at {episode_data["audio"]}')
