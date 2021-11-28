import slack
from django.db import models
from django_simple_slack_app.info_cache import slack_cache


class SlackTeam(models.Model):
    id = models.CharField("Team Slack-ID", max_length=64, primary_key=True, null=False)
    name = models.CharField("Team Name", max_length=1024, null=True)

    info = models.TextField("Team Info", null=True)

    updated_at = models.DateTimeField("created time", auto_now=True)
    created_at = models.DateTimeField("created time", auto_now_add=True)

    def __str__(self):
        return f"[{self.id}] {self.name}"

    def update_info(self):
        self.info = slack_cache.get('team', self.id)
        self.save()


class SlackUser(models.Model):
    id = models.CharField("User Slack-ID", max_length=64, primary_key=True, null=False)
    token = models.CharField("User Access Token", max_length=1024, unique=True, null=False)

    info = models.TextField("User Info", null=True)
    team = models.ForeignKey(SlackTeam, null=False, blank=False, on_delete=models.CASCADE)

    updated_at = models.DateTimeField("created time", auto_now=True)
    created_at = models.DateTimeField("created time", auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = None

    def set_default_channel(self, channel):
        self.channel = channel

    def __str__(self):
        return f"{self.id} in {self.team}"

    def get_client(self):
        return slack.WebClient(token=self.token)

    def post_message(self, **kwargs):
        if 'channel' not in kwargs:
            kwargs['channel'] = self.channel

        self.get_client().chat_postMessage(**kwargs)

    def chat_update(self, **kwargs):
        if 'channel' not in kwargs:
            kwargs['channel'] = self.channel

        self.get_client().chat_update(**kwargs)

    def update_info(self):
        self.info = slack_cache.get('user', self.id)
        self.save()
