from django.db import models
from django.conf import settings

# Create your models here.

class Mood(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Content(models.Model):
    CONTENT_CHOICES = (
        ('music', 'MUSIC'),
        ('video', 'VIDEO'),
        ('quote', 'QUOTES')
    )

    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255, choices=CONTENT_CHOICES)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    url = models.URLField()
    text = models.TextField()

    def __str__(self):
        return self.title

class History(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    view_at = models.DateTimeField(auto_now=True)

class Favorites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    