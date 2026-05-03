import requests
from django.conf import settings
import base64

def fetch_youtube_videos(mood):
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": f"{mood} music OR {mood} video",
        "key": settings.YOUTUBE_API_KEY,
        "maxResults": 5,
        "type": "video"
    }

    response = requests.get(url, params=params)

    results = []

    if response.status_code == 200:
        data = response.json()

        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]

            video_data = {
                "title": snippet["title"],
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": snippet["thumbnails"]["high"]["url"],
                "channel": snippet["channelTitle"],
            }

            results.append(video_data)

    return results


def get_spotify_token():

    url = "https://accounts.spotify.com/api/token"

    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET


    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)


    if response.status_code == 200:
        return response.json().get("access_token")

    return None



def fetch_spotify_tracks(mood):
    token = get_spotify_token()

    if not token:
        print("No spotify token")
        return []

    print("TOKEN LENGTH:", len(token))
    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": f"{mood} music",
        "type": "track",
        "limit": 5
    }

    response = requests.get(url, headers=headers, params=params)

    results = []

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code == 200:
        data = response.json()

        for item in data["tracks"]["items"]:
            track = {
                "title": item["name"],
                "artist": item["artists"][0]["name"],
                "url": item["external_urls"]["spotify"],
                "preview": item["preview_url"],  # can be None
                "image": item["album"]["images"][0]["url"]
            }

            results.append(track)

    return results