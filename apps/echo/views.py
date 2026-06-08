import json
from datetime import datetime, timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def echo(request):
    """
    Endpoint echo — memantulkan kembali semua detail request yang masuk.
    Berguna untuk debugging client, memahami struktur HTTP request,
    dan eksplorasi header / body.
    """
    body = None
    if request.body:
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            body = request.body.decode("utf-8", errors="replace")

    return Response({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "method": request.method,
        "path": request.path,
        "full_url": request.build_absolute_uri(),
        "query_params": dict(request.GET),
        "headers": dict(request.headers),
        "body": body,
        "client": {
            "host": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
        },
    })
