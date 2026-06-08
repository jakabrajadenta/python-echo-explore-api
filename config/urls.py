from django.urls import path, include

urlpatterns = [
    path("", include("apps.health.urls")),
    path("", include("apps.echo.urls")),
    path("api/v1/users/", include("apps.users.urls")),
]
