import spotipy
from spotipy.oauth2 import SpotifyOAuth


def instantiate_spotify():
    scope = "user-library-read user-read-playback-position"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp


def list_subscibed_shows(sp):
    shows = sp.current_user_saved_shows()
    results = []
    for item in shows['items']:
        show = item['show']
        result = {
            'id': show['id'],
            'name': show['name']
        }
        results.append(result)
    return results


def list_last_episodes(sp, show):
    """
    Get the id of the last 20 episodes of the selected show
    """
    episodes = []
    data = sp.show_episodes(show['id'], limit=20)
    for episode in data['items']:
        result = {
            'id': episode['id'],
            'name': episode['name'],
            'show_name': show['name'],
            'duration_ms': episode['duration_ms'],
            'resume_point': episode['resume_point'],
        }
        episodes.append(result)
    return episodes


def list_show_episodes(sp, shows):
    """
    Get the last of every show
    """
    episodes = []
    for show in shows:
        show_episodes = list_last_episodes(sp, show)
        episodes += show_episodes
    return episodes


def filter_episodes(episodes):
    """
    Filter down to episodes that the user listened to
    """

    def has_been_listened(episode):
        resume_point = episode.get('resume_point', None)
        if not resume_point:
            return False

        if resume_point['fully_played']:
            return True

        percentage_listened = (resume_point['resume_position_ms'] / episode['duration_ms']) * 100
        return percentage_listened > 50

    return [episode for episode in episodes if has_been_listened(episode)]


def get_latest_user_episodes():
    sp = instantiate_spotify()
    shows = list_subscibed_shows(sp)
    episodes = list_show_episodes(sp, shows)
    return filter_episodes(episodes)