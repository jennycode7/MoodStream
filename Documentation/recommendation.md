# Recommendations

The Recommendation endpoint delivers personalized content to users based on their current mood or their preferred mood.

---

## Get Recommendations

Retrieve content tailored to a user's mood.

**Endpoint:**

```http id="m9y7q1"
GET /recommendations/
```

---

## Query Parameters

| Parameter | Type   | Required | Description                                       |
| --------- | ------ | -------- | ------------------------------------------------- |
| mood      | string | Yes       | Mood to filter content (overrides preferred mood) |
| type      | string | Yes       | Filter by content type                            |

---

## Supported Moods

* happy
* sad
* relaxed
* energetic
* anxious

---

## Supported Content Types

* music
* movie
* quote

---

## How It Works

1. If `mood` is provided → use it
2. If not → fallback to user's `preferred_mood`
3. Filter content by:

   * mood
   * optional content type
4. Return matching results

---

## Example Requests

### Using Custom Mood

```http id="r6g1dz"
GET /recommendations/?mood=happy
```

---

### Using Preferred Mood (No Query)

```http id="7j0m3t"
GET /recommendations/
```

---

### Filter by Mood + Type

```http id="7f8k2a"
GET /recommendations/?mood=relaxed&type=music
```

---

## Response

```json id="g2zvkw"
[
  {
    "id": 12,
    "title": "Chill Vibes Playlist",
    "content_type": "music",
    "mood": "relaxed",
    "url": "content_url"
  },
  {
    "id": 18,
    "title": "Feel Good Movie",
    "content_type": "movie",
    "mood": "happy",
    "url", "content_url"
  }
]
```

---

## Personalized Behavior

* If no `mood` is passed, the system automatically uses the user's **preferred_mood**
* Results are always scoped to what matches the user's emotional context

---

## Edge Cases

### No Matching Content

```json id="4ndn5g"
{
  "message": "No content found for this mood"
}
```

---

### Invalid Mood

```json id="dxk2o9"
{
  "error": "Invalid mood value"
}
```

---

### Unauthorized

```json id="nd2w4r"
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Authentication Required

This endpoint requires authentication.

Include your token:

```http id="l2x8zq"
Authorization: Bearer <your_access_token>
```

---

## Future Improvements (Optional)

* AI-based recommendations
* Trending content by mood
* User behavior learning (likes, skips)
* Time-based mood suggestions

---
