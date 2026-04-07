import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all().order_by("-created_at")
    serializer_class = ActivitySerializer


@api_view(["GET"])
def github_activity(request):
    username = "your-github-username"

    url = f"https://api.github.com/users/{username}/events"
    res = requests.get(url)

    if res.status_code != 200:
        return Response({"error": "GitHub API failed"}, status=400)

    data = res.json()

    formatted = []
    for event in data[:10]:
        formatted.append({
            "type": "github",
            "title": event["type"],
            "repo": event["repo"]["name"],
        })

    return Response(formatted)