import hgtk
import slack

from django_slack_app import slack_events

SLACK_BOT_USER_TOKEN = "??"
client = slack.WebClient(token=SLACK_BOT_USER_TOKEN)


@slack_events.on("reaction_added")
def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    print(f"New reaction: {emoji}")


@slack_events.on("message")
def message_channels(event_data):
    msg = event_data["event"]["text"]
    print(f"New message: {msg}")
