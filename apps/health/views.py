import psycopg2
from datetime import datetime, timezone
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    """Endpoint health check — cek koneksi database dan status service."""
    db_status = "ok"
    db_error = None

    db = settings.DATABASES["default"]
    try:
        conn = psycopg2.connect(
            dbname=db["NAME"],
            user=db["USER"],
            password=db["PASSWORD"],
            host=db["HOST"],
            port=db["PORT"],
        )
        conn.close()
    except Exception as exc:
        db_status = "error"
        db_error = str(exc)

    return Response({
        "status": "ok" if db_status == "ok" else "degraded",
        "service": "Python Echo Explore API",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dependencies": {
            "database": {
                "status": db_status,
                **({"error": db_error} if db_error else {}),
            }
        },
    })
