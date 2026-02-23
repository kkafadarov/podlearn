from spotify_utils import get_latest_user_episodes
from podindex import *
from audio_downloader import download_audio, sanitize_filename
from transcript_generator import get_transcripts
from dotenv import load_dotenv

# Load environment variables from .secrets file
load_dotenv('.secrets')


if __name__ == "__main__":
    user_episodes = get_latest_user_episodes()
    episodes_to_downwload = match_episodes(user_episodes)
    for show_name, watched_episodes in episodes_to_downwload.items():
        for episode in watched_episodes:
            filename = sanitize_filename(show_name + '_' +episode['title'])
            download_audio(url = episode['audio_href'], filename=filename)