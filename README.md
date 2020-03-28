# django-simple-slack-app

## Intro
Yet another django slack app(bot) package!

Integrate your django app with Slack app using simple and beautiful django-way that support brand new **Slack Event API** and **OAuth**.

#### thanks to
the core part of this project has based on the 
- [slackapi/python-slackclient](https://github.com/slackapi/python-slackclient)
- [slackapi/python-slack-events-api](https://github.com/slackapi/python-slack-events-api)

that is the official slack API packages.

# Requirement
- Python 3.6+
- Django 2+

## Features (TODO)

- [x] OAuth Redirect handling (response verifying & token DB managing)
- [ ] Interactive Component
- [x] Slach Command
- [x] Event Subscription 

### And... we're not gonna support:
- Incoming Webhook
- Classic App and RTM

## install

### 1. install package
```bash
$ pip install -e https://github.com/bluedisk/django-slack-app.git
```

### 2. update settings.py
```python

INSTALLED_APPS = [
    
    ...

    'django_simple_slack_app'  # add here!

    ...
    'my_slack_app'  # your app
]

```

And
```python
 
SLACK_EVENT_URL = 'events'  # default
SLACK_OAUTH_URL = 'oauth'  # default
SLACK_COMMAND_URL = 'commands'  # default

SLACK_EVENTS = "my_slack_app.slack_events"  # the module that you want to handle the event
SLACK_SIGNING_SECRET = "SOMENICESECRETCODE"  # your slack-app's secret

```

```SLACK_OAUTH_URL``` and ```SLACK_OAUTH_URL``` in the above code are a same with default url. so, you can skip it. I just write it to show you the default URL explicitly.

### 3. add route to the django-slack-app
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    
    ...

    path('slack/', include("django_simple_slack_app.urls")),
]

```
In this case, 
- Your event-subscription URL is "http://yourdomain/slack/events"
- Your slash-command URL is  "http://yourdomain/slack/commands" 
- Your OAuth redirect URL is  "http://yourdomain/slack/oauth" 

* you have set the URLs on the slack app configuration in the slack SDK page.


### 4. implement event handler
see the link for the details https://api.slack.com/events-api

**my_slack_app/slack_events.py**
```python
from django_simple_slack_app import slack_events


@slack_events.on("reaction_added")
def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    print(f"New reaction: {emoji}")


@slack_events.on("message")
def message_channels(event_data):
    msg = event_data["event"]["text"]
    print(f"New message: {msg}")
```

now, you can get slack events!

typical message event looks like:
```json
{
    "api_app_id": "AUG7U9D47",
    "authed_users": [
        "UUZBJLZZV"
    ],
    "event": {
        "blocks": [
            {
                "block_id": "X7A",
                "elements": [
                    {
                        "elements": [
                            {
                                "text": "test",
                                "type": "text"
                            }
                        ],
                        "type": "rich_text_section"
                    }
                ],
                "type": "rich_text"
            }
        ],
        "channel": "CFSW8SJZ1",
        "channel_type": "channel",
        "client_msg_id": "8af7be2cd-4334-3e2-a601-32e33337e2f0",
        "event_ts": "1585396328.000300",
        "team": "TFXP2Z7GQ",
        "text": "test",
        "ts": "1585396328.000300",
        "type": "message",
        "user": "UFFKGQZQ1"
    },
    "event_id": "Ev010YJAAT6Y",
    "event_time": 1585396328,
    "team_id": "TFXP2Z7GQ",
    "token": "tb5VWK0vVzMqavhbOpwYB5kA",
    "type": "event_callback"
}
```


### 5. implement slash command

you need to add slash-command and set the endpoint for that on the slack app setting before start to impelement it.

see the link for the detail about the slash-command https://api.slack.com/interactivity/slash-commands

**my_slack_app/slack_events.py**
```python
from django_simple_slack_app import slack_events, slack_commands

...


@slack_commands.on("/myapp")
def my_command(event_data):
    print(f"Command {event_data['command']} has received")


# if you want to get the sub-command, enter the sub-command with comma after the command name
@slack_commands.on("/myapp.subcommand")
def my_command(event_data):
    print(f"Command {event_data['command']} has received")

```

typical slash command has the following data:
```json
{
    'channel_id': 'CF86ZSRHS',
    'channel_name': 'some channel',
    'command': '/myapp',
    'response_url': 'https://hooks.slack.com/commands/TFGXQ1P37/1021528680361/g7Mda8uCjrP8WO13AsVbSFHj',
    'team_domain': 'my-team',
    'team_id': 'TFGXQ1P37',
    'text': 'subcommand 123',
    'token': 'tbkAVWYc43VzWkavB5nK0v5Mh',
    'trigger_id': '1033087519408.526847057041.0cdd28da169b45ecfcb1ee783f5d22fb',
    'user_id': 'U3FG14FK',
    'user_name': 'myuserid'
}
```

## FAQ
### What is the difference between this and others?
other libraries are:
- hard to use
- not integrated with Django
- includes unnecessary dependencies(like a flask)
- not support OAuth 
- or Developer have to manage the OAuth tokens
- NOT SUPPORT EVENT SUBSCRIPTION ** most important reason **
