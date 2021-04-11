from spotify_utils import get_latest_user_episodes
from transcript_generator import get_transcripts

if __name__ == "__main__":
    user_episodes = get_latest_user_episodes()
    transcripts = get_transcripts(user_episodes)
    [print(transcript) for transcript in transcripts]
