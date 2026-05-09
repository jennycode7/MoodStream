from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import MoodSerializer, HistorySerializer, FavoritesSerializer, ContentSerializer, RecommendationSerializer
from .models import Mood, History, Favorites, Content
from .services import get_recommendations
from drf_spectacular.utils import extend_schema

# Create your views here.

class RecommendationView(generics.GenericAPIView):
    permission_class = [IsAuthenticated]
    serializer_class = RecommendationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        # create Mood instance
        data = serializer.save()

        mood = data['mood']
        content_type = data['content_type']

        # (Optional) Save user's last selected mood
        request.user.preferred_mood = mood.name
        request.user.save()

        # Get recommendations
        results = get_recommendations(request.user, mood, content_type)

        # Save history (only DB content)
        history_objects = []

        for item in results:
            content = Content.objects.filter(url=item["url"]).first()

            if content:
                history_objects.append(
                    History(
                        user=request.user,
                        content=content
                    )
                )

        History.objects.bulk_create(history_objects)

        return Response({
            "user": request.user.username,
            "mood": mood.name,
            "results": results
        }, status=status.HTTP_200_OK)

class MoodView(generics.ListAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    permission_class = [IsAuthenticated]

    
class HistoryView(generics.ListAPIView):
    queryset = History.objects.all()    
    serializer_class = HistorySerializer
    permission_class = [IsAuthenticated]


class FavoritesView(generics.ListCreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_class = [IsAuthenticated]

class ContentView(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_class = [IsAuthenticated]
