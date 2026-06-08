from django.db import models


class User(models.Model):
    """
    Memetakan ke tabel user_management.users yang sudah dibuat via sql/ddl.sql.
    managed=False → Django tidak akan membuat/mengubah tabel ini lewat migrasi.
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, default="", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = '"user_management"."users"'
        ordering = ["id"]

    def __str__(self):
        return f"{self.username} <{self.email}>"
