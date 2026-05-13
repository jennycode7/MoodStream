# MoodStream API Documentation

Welcome to the MoodStream API 🎧

MoodStream is a mood-based content recommendation API that allows users to discover and save content such as music, movies, and quotes based on their emotions.

---

## 🔗 Base URL

```
https://mood-stream.six.vercel.app/api/docs
```

---

## 📚 Documentation Sections

* [Authentication](authentication.md)
* [Users](users.md)
* [Content](content.md)
* [Favorites](favorites.md)
* [Moods](moods.md)
* [Error Handling](errors.md)
* [Setup Guide](setup.md)

---

## 🚀 Quick Start

1. Register a user
2. Login to get JWT token
3. Use token for authenticated endpoints
4. Explore content based on mood
5. Save favorites

---

## 🔐 Authentication Type

This API uses **JWT Authentication**

Include token in headers:

```
Authorization: Bearer <your_token>
```
