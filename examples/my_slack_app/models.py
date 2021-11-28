from django.db import models

from django_simple_slack_app.models import AbstractSlackUser, SlackUser


class MySlackUser(models.Model):
    user = models.OneToOneField(SlackUser, on_delete=models.CASCADE)
    enabled = models.BooleanField("Is Enabled", default=True)
