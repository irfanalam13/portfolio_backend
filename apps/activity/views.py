import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer

GITHUB_CACHE_TTL = 60 * 30  # 30 minutes (GitHub anon limit is 60 req/hour)


class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all().order_by("-created_at")
    serializer_class = ActivitySerializer


@api_view(["GET"])
def github_activity(request):
    """Return recent public GitHub events, cached to respect rate limits.

    On any failure (no username configured, network error, GitHub down) we
    return an empty list so the frontend's static fallback takes over instead
    of surfacing an error.
    """
    username = getattr(settings, "GITHUB_USERNAME", "")
    if not username:
        return Response([])

    cache_key = f"github_activity:{username}"
    cached = cache.get(cache_key)
    if cached is not None:
        return Response(cached)

    url = f"https://api.github.com/users/{username}/events/public"
    try:
        res = requests.get(
            url,
            timeout=5,
            headers={"Accept": "application/vnd.github+json"},
        )
        res.raise_for_status()
        data = res.json()
    except (requests.RequestException, ValueError):
        return Response([])

    formatted = [
        {
            "type": "github",
            "title": event.get("type"),
            "repo": event.get("repo", {}).get("name"),
        }
        for event in data[:10]
    ]

    cache.set(cache_key, formatted, GITHUB_CACHE_TTL)
    return Response(formatted)