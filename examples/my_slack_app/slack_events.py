from pprint import pprint

import slack
from django.conf import settings

from django_simple_slack_app import slack_events
from django_simple_slack_app.models import SlackUser

client = slack.WebClient(token=settings.SLACK_BOT_USER_TOKEN)


# slack event handling

@slack_events.on("reaction_added")
def reaction_added(event_data, user):
    emoji = event_data["event"]["reaction"]
    print(f"New reaction: {emoji}")


@slack_events.on("message")
def message_channels(event_data, user):
    event = event_data['event']
    msg = event["text"]
    print(f"New message: {msg}")

    # if user has authorized, the event has a SlackUser object and slack WebClient for the token
    if isinstance(event['user'], SlackUser):
        print(f"Authorized user!")
        pprint(event['user'])

        user.post_message(text="I said, " + msg)


# django-simple-slack-app event handling
@slack_events.on("error")
def on_event_error(error):
    print("Error caused for ", end="")
    pprint(error)


@slack_events.on("oauth")
def on_event_error(user):
    print("OAuth finished for ", end="")
    pprint(user)
