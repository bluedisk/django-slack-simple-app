import slack
from django.conf import settings
from django.core.cache import cache
from pprint import pprint
from slack.errors import SlackApiError


class SlackInfo:

    def __init__(self, id, name, content, client=None):
        self.content = content
        self.id = id
        self.name = name
        self.client = client

    def __str__(self):
        return f"[{self.id}] {self.name}"

    def info(self, field_name):
        return self.content.get(field_name, None)

    def profile(self, field_name):
        return self.info(field_name)


class SlackCacheManager:
    def __init__(self):
        pass

    @staticmethod
    def get(info_type, id):
        key = f"slack:{info_type}:{id}"
        info = cache.get(key)
        if not info:
            client = slack.WebClient(token=settings.SLACK_APP_BOT_TOKEN)
            try:
                if info_type == 'user':
                    info = client.users_profile_get(user=id).data.get('profile')
                elif info_type == 'channel':
                    info = client.conversations_info(channel=id).data.get('channel')
                elif info_type == 'team':
                    info = client.team_info(team=id).data.get('team')
                else:
                    raise RuntimeError

                cache.set(key, info)
            except SlackApiError as e:
                pprint(e)
                info = {"name": f"{info_type}-{id}"}

        return info


slack_cache = SlackCacheManager()
