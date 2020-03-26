import slack

from django_slack_app import slack_events, slack_commands

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


@slack_commands.on("/myapp")
def my_command(event_data):
    print(f"Command {event_data['command']} has received")


# if you want to get the sub-command, enter the sub-command with comma after the command name
@slack_commands.on("/myapp.subcommand")
def my_command(event_data):
    print(f"Command {event_data['command']} has received")
