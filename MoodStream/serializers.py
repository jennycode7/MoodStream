from rest_framework import serializers
from .models import Mood, Content, Favorites, History



class MoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mood
        fields = ['name']

class RecommendationSerializer(serializers.Serializer):
    mood = serializers.CharField()
    content_type = serializers.ChoiceField(choices=["video", "music", "quote"])


    def validate_mood(self, value):
        return value.strip().lower()

    def validate_content_type(self, value):
        # ensure consistency with your logic layer
        return value.strip().lower()
    

    def create(self, validated_data):
        mood_name = validated_data["mood"].strip().lower()

        mood = Mood.objects.filter(name__iexact=mood_name).first()

        if not mood:
            mood = Mood.objects.create(name=mood_name)

        return {
                "mood": mood,
                "content_type": validated_data["content_type"]
            }



class ContentSerializer(serializers.ModelSerializer):
    mood = serializers.CharField(source="mood.name")


    class Meta:
        model = Content
        fields = '__all__'

class FavoritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorites
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'