from django.db import models

from django_simple_slack_app.models import AbstractSlackUser


class MySlackUser(AbstractSlackUser):
    enabled = models.BooleanField("Is Enabled", default=True)
