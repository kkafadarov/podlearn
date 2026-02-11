import requests
import sys


def download_audio(url, filename):
    response = requests.get(url, allow_redirects=True)
    with open("audio_files/" + filename + ".mp3", 'wb') as f:
        f.write(response.content)


if __name__ == "__main__":
    download_audio(sys.argv[1], sys.argv[2])
