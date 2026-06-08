from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import IntegrityError
from .models import User
from .serializers import UserSerializer, UserWriteSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD untuk User.

    GET    /api/v1/users/       → list   (query: skip, limit, is_active)
    POST   /api/v1/users/       → create
    GET    /api/v1/users/{id}/  → retrieve
    PUT    /api/v1/users/{id}/  → full update   (semua field wajib)
    PATCH  /api/v1/users/{id}/  → partial update (hanya field yang dikirim)
    DELETE /api/v1/users/{id}/  → delete
    """

    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserWriteSerializer
        return UserSerializer

    # ── List dengan manual pagination & filter ────────────────────────────────

    def list(self, request, *args, **kwargs):
        qs = User.objects.all()

        is_active_param = request.query_params.get("is_active")
        if is_active_param is not None:
            qs = qs.filter(is_active=is_active_param.lower() == "true")

        try:
            skip = max(0, int(request.query_params.get("skip", 0)))
            limit = min(max(1, int(request.query_params.get("limit", 10))), 100)
        except ValueError:
            skip, limit = 0, 10

        serializer = UserSerializer(qs[skip: skip + limit], many=True)
        return Response(serializer.data)

    # ── Create ────────────────────────────────────────────────────────────────

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"detail": "Username atau email sudah digunakan."},
                status=status.HTTP_409_CONFLICT,
            )

    # ── Update (PUT & PATCH) ──────────────────────────────────────────────────

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            return Response(UserSerializer(user).data)
        except IntegrityError:
            return Response(
                {"detail": "Username atau email sudah digunakan."},
                status=status.HTTP_409_CONFLICT,
            )

    # ── Delete ────────────────────────────────────────────────────────────────

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
