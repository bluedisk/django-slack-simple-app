from django.contrib.auth import get_user_model
from django.db import models


class AbstractSlackUser(models.Model):
    class Meta:
        abstract = True

    user = models.CharField("Slack User ID", max_length=1024, primary_key=True, null=False)
    token = models.CharField("User Access Token", max_length=1024, unique=True, null=False)

    team_id = models.CharField("Team ID", max_length=1024, null=True)
    team_name = models.CharField("Team Name", max_length=1024, null=True)

    created_at = models.DateTimeField("created time", auto_now_add=True)

    def __str__(self):
        return self.user


class SlackUser(AbstractSlackUser):
    pass
