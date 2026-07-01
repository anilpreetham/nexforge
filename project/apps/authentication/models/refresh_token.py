from django.db import models
from .user import CustomUser


class RefreshToken(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="refresh_tokens"
    )

    token = models.TextField()

    expires_at = models.DateTimeField()

    is_revoked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "refresh_tokens"

    def __str__(self):
        return self.user.username