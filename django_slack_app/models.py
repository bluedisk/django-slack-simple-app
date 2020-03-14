from django.contrib.auth import get_user_model
from django.db import models


class UserToken(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="tokens", on_delete=models.CASCADE, primary_key=True,
                             null=False)
    token = models.CharField("User Access Token", max_length=1024, unique=True, null=False)

    created_at = models.DateTimeField("created time", auto_now_add=True)
