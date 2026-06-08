from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer untuk response — menampilkan semua field termasuk timestamp."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name", "phone", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserWriteSerializer(serializers.ModelSerializer):
    """
    Serializer untuk create (POST) dan update (PUT/PATCH).
    - POST / PUT : username, email, full_name wajib diisi
    - PATCH      : semua field opsional (partial=True otomatis dari ViewSet)
    Response selalu menggunakan UserSerializer agar format konsisten.
    """
    phone = serializers.CharField(max_length=20, default="", allow_blank=True, required=False)
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = User
        fields = ["username", "email", "full_name", "phone", "is_active"]

    def to_representation(self, instance):
        return UserSerializer(instance, context=self.context).data
