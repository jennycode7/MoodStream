from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import MoodSerializer
from .models import Mood, History
from .services import get_recommendations

# Create your views here.

class RecommendationView(GenericAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = MoodSerializer

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
        History.objects.bulk_create([
            History(user=request.user, content_id=item["id"])
            for item in results if item.get("id")
        ])

        print("RAW:", request.data.get("content_type"))
        print("VALIDATED:", serializer.validated_data.get("content_type"))

        return Response({
            "mood": mood.name,
            "results": results
        }, status=status.HTTP_200_OK)
    