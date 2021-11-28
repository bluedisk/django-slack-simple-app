import requests

from django_simple_slack_app import slack_commands


# slash command handling
@slack_commands.on("/myapp")
def my_command(event_data, user, response):
    print(f"Command {event_data['command']} has received")
    response.ephemeral({
        "text": f"My slack app received slash-command {event_data['command']} from {user.name}"
                        })


# if you want to get the sub-command, enter the sub-command with comma after the command name
@slack_commands.on("/myapp.subcommand")
def my_command(event_data, user, response):
    print(f"Command {event_data['command']} has received")
    response.ephemeral({
        "text": f"My slack app received slash-command %s with subcommand {event_data['command']} from {user.name}"
    })
