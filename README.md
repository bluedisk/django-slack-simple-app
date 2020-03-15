# django-slack-app

## Intro
Yet another django slack app(bot) package!

core part of this project has based 
on the [slackapi/python-slackclient](https://github.com/slackapi/python-slackclient)
and [slackapi/python-slack-events-api](https://github.com/slackapi/python-slack-events-api)
that is the official slack api packages.

## Features (TODO)

[x] OAuth Redirect handling (response checking & update token DB)
[ ] Interactive Component
[ ] Slach Command
[x] Event Subscription 

### And... we're not gonna support:
- Incoming Webhook
- Classic App and RTM

## install

1. install package
```bash
$ pip install django-slack-app 
```

2. update settings.py
```python

INSTALLED_APPS = [
    
    ...

    'django_slack_app'  # add here!

    ...
    'my_slack_app'
]

```

And
```python

SLACK_EVENTS = "my_slack_app.slack_events"
SLACK_SIGNING_SECRET = "SOMENICESECRETCODE"

```

3. add route to the django-slack-app
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    
    ...

    path('slack/events', include("django_slack_app.urls")),
]

```

4. implement event handler

**my_slack_app/slack_events.py**
```python
from django_slack_app import slack_events


@slack_events.on("reaction_added")
def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    print(f"New reaction: {emoji}")


@slack_events.on("message")
def message_channels(event_data):
    msg = event_data["event"]["text"]
    print(f"New message: {msg}")
```

now, you can get the events!


## FAQ
### What is diffrent between this and others?
other libraries are:
- hard to use
- not integrated with django
- includes unnessesary dependancies(like a flask)
- not support OAuth 
- or Deveolper have to manage the OAuth tokens
- NOT SUPPORT EVENT SUBSCRIPTION ** most important reasone **