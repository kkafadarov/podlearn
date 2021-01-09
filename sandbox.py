import spotipy
from spotipy.oauth2 import SpotifyOAuth


def list_subscibed_shows():
    scope = "user-library-read user-read-playback-position"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    shows = sp.current_user_saved_shows()
    results = []
    for item in shows['items']:
        show = item['show']
        result = {
            'id': show['id'],
            'name':show['name']
        }
        results.append(result)
    return results

if __name__ == "__main__":
    results=list_subscibed_shows()
    print(results)
