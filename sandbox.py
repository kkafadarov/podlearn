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
        result =  {
            'id': episode['id'],
            'name': episode['name'],
            'duration_ms': episode['duration_ms'],
            'resume_point': episode['resume_point']

        }
        episodes.append(result)
    return episodes

def list_shows(sp,shows):
    """
    Get the last of every show
    """
    episodes = []
    for show in shows:
        show_episodes =list_last_episodes(sp, show)
        episodes += show_episodes
    return episodes

def filter_episodes(sp,episodes):
    """
    Filter unwatched episodes, return only watched >50%
    """
    filtrd_episodes = []
    for episode in episodes:
        duration = episode['duration_ms']
        resume_point = episode['resume_point']
        if resume_point['fully_played']:
           filtrd_episodes.append(episode)
        elif resume_point['resume_position_ms'] > duration / 2 :
            filtrd_episodes.append(episode)
    return filtrd_episodes

if __name__ == "__main__":
    sp = instantiate_spotify()
    shows = list_subscibed_shows(sp)
    episodes = list_shows(sp,shows)
    episodes = filter_episodes(sp,episodes)
    print(episodes)
