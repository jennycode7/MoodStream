import random
import requests
from django.conf import settings
from .models import Content, History, Mood
from .external_api import fetch_youtube_videos, fetch_spotify_tracks


def fetch_external_content(mood, content_type):
    results = []

    try:
        # get or create mood
        # mood_obj = Mood.objects.filter(name__iexact=mood).first()

        # if not mood_obj:
        #     mood_obj = Mood.objects.create(name=mood)

        if isinstance(mood, Mood):
            mood_obj = mood
        else:
            mood_obj = Mood.objects.filter(name__iexact=mood).first()
            
            if not mood_obj:
                mood_obj = Mood.objects.create(name=mood)



        #  VIDEO
        if content_type == "video":
            youtube_results = fetch_youtube_videos(mood_obj)


            for item in youtube_results:
                content, _ = Content.objects.get_or_create(
                    url=item['url'],
                    defaults={
                        "title": item['title'],
                        "content_type": "video",
                        "mood": mood_obj
                    }
                )

                results.append({
                    'id': content.id,
                    "title": content.title,
                    "url": content.url,
                    "thumbnail": item['thumbnail']
                })

        #  SONG
        elif content_type == "music":
            spotify_results = fetch_spotify_tracks(mood_obj)

            for item in spotify_results:
                content, _ = Content.objects.get_or_create(
                    url=item['url'],
                    defaults={
                        "title": item['title'],
                        "content_type": "song",
                        "mood": mood_obj
                    }
                )

                results.append({
                    "id": content.id,
                    "title": item["title"],
                    "artist": item["artist"],
                    "url": item["url"],
                    "preview": item["preview"],
                    "image": item["image"]
                })
    

        # QUOTES
        elif content_type == "quote":
            response = requests.get("https://zenquotes.io/api/random", timeout=5)

            if response.status_code == 200:
                data = response.json()[0]
                quote_text = data.get("q")
                author = data.get("a")

                if not quote_text:
                    return results

                url = f"https://zenquotes.io/?q={quote_text}"

                content, _ = Content.objects.get_or_create(
                    text=quote_text,
                    defaults={
                        "title": quote_text[:50],
                        "content_type": "quote",
                        "url": url,
                        "mood": mood_obj
                    }
                )

                results.append({
                    "text": quote_text,
                    "author": author,
                    "url": content.url
                })

        else:
            print("ZenQuotes API error:", response.text)

    except Exception as e:
        print("ERROR:", str(e))

    return results



def get_recommendations(user, mood_name, content_type):

    if isinstance(mood_name, Mood):
        mood_name = mood_name.name


    contents = Content.objects.filter(
        mood__name__iexact=mood_name,
        content_type=content_type
    )

    seen_ids = History.objects.filter(user=user).values_list('content_id', flat=True)
    contents = contents.exclude(id__in=seen_ids)

    # 3. Fallback
    if not contents.exists():
        contents = Content.objects.filter(
            mood__name__iexact=mood_name,
            content_type=content_type
        )

    db_results = list(contents)

    # 4. Random selection
    if db_results:
        db_results = random.sample(db_results, min(7, len(db_results)))

    # 5. Format DB → URL only
    db_urls = [
        {"id": item.id, "url": item.url}
        for item in db_results if item.url
    ]

    # 6. External content
    external_urls = fetch_external_content(mood_name, content_type)

    # 7. Combine
    return db_urls + external_urls