import random
import requests
from django.conf import settings
from .models import Content, History, Mood



def fetch_external_content(mood, content_type):
    results = []

    try:
        # get or create mood
        mood_obj = Mood.objects.filter(name__iexact=mood).first()

        if not mood_obj:
            mood_obj = Mood.objects.create(name=mood)
        print('check here')
        #  VIDEO
        if content_type == "video":
            url = f"https://www.youtube.com/results?search_query={mood}+{content_type}"

            content, _ = Content.objects.get_or_create(
                url=url,
                defaults={
                    "title": f"{mood} video",
                    "content_type": "video",
                    "mood": mood_obj
                }
            )

            results.append({"url": content.url})

        #  SONG
        elif content_type == "music":
            print('music check')
            url = f"https://open.spotify.com/search/{mood.name}%20music"

            content, _ = Content.objects.get_or_create(
                url=url,
                defaults={
                    "title": f"{mood} song",
                    "content_type": "song",
                    "mood": mood_obj
                }
            )

            results.append({"url": content.url})
    

        # QUOTES
        elif content_type == "quote":
            response = requests.get("https://zenquotes.io/api/random", timeout=5)

            if response.status_code == 200:
                data = response.json()[0]
                quote_text = data.get("q")

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

                results.append({"url": content.url})

        else:
            print("INVALID CONTENT TYPE:", content_type)

    except Exception:
        pass

    print("music ended")
    return results



def get_recommendations(user, mood_name, content_type):
    # 1. DB content
    contents = Content.objects.filter(
        mood__name__iexact=mood_name,
        content_type=content_type
    )

    # 2. Remove seen
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