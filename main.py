from spotify_utils import get_latest_user_episodes
from transcript_generator import get_transcripts
from dotenv import load_dotenv

# Load environment variables from .secrets file
load_dotenv('.secrets')


if __name__ == "__main__":
    user_episodes = get_latest_user_episodes()
    transcripts = get_transcripts(user_episodes)
    [print(transcript) for transcript in transcripts]
