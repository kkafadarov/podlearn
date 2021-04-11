from listen_notes_api import find_podcast_episode, EpisodeNotFoundError


def get_transcript(episode):
    # TODO: 1) check if episode[id] already has a transcript in the DB
    # 2) if not, get metadata from ListenNotes
    try:
        episode_data = find_podcast_episode(episode['name'], episode['show_name'])
    except EpisodeNotFoundError:
        error = f"{episode['show_name']}: {episode['name']} not found - needs manual intervention"
        print(error)
        return error

    # 3) if listen notes has a transcript, return it
    if episode_data.get("transcript", None):
        return episode_data["transcript"]

    # TODO: 4) otherwise generate it from the audiofile
    return f'To be generated from: {episode_data["audio"]}'


def get_transcripts(episodes):
    return [get_transcript(episode) for episode in episodes]
