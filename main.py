from spotify_utils import instantiate_spotify, list_subscibed_shows, list_shows

if __name__ == "__main__":
    sp = instantiate_spotify()
    shows = list_subscibed_shows(sp)
    episodes = list_shows(sp,shows)
    print(episodes)
