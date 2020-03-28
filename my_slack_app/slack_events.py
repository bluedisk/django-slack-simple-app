from pprint import pprint

import slack

from django_simple_slack_app import slack_events, slack_commands
from django_simple_slack_app.models import SlackUser

SLACK_BOT_USER_TOKEN = "??"
client = slack.WebClient(token=SLACK_BOT_USER_TOKEN)


@slack_events.on("reaction_added")
def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    print(f"New reaction: {emoji}")


@slack_events.on("message")
def message_channels(event_data):
    event = event_data['event']
    msg = event["text"]
    print(f"New message: {msg}")

    # if user has authorized, the event has a SlackUser object and slack WebClient for the token
    if isinstance(event['user'], SlackUser):
        print(f"Authorized user!")
        pprint(event['user'])

        event['client'].chat_postMessage(channel=event['channel'], text="I said, " + msg)


@slack_commands.on("/myapp")
def my_command(event_data):
    print(f"Command {event_data['command']} has received")


# if you want to get the sub-command, enter the sub-command with comma after the command name
@slack_commands.on("/myapp.subcommand")
def my_command(event_data):
    print(f"Command {event_data['command']} has received")
