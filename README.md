# django-slack-app

## Intro
Yet another django slack app(bot) package!

core part of this project has based on the 
- [slackapi/python-slackclient](https://github.com/slackapi/python-slackclient)
- [slackapi/python-slack-events-api](https://github.com/slackapi/python-slack-events-api)

that is the official slack API packages.

## Features (TODO)

- [x] [WIP] OAuth Redirect handling (response verifying & token DB managing)
- [ ] Interactive Component
- [ ] Slach Command
- [x] Event Subscription 

### And... we're not gonna support:
- Incoming Webhook
- Classic App and RTM

## install

1. install package
```bash
$ pip install -e https://github.com/bluedisk/django-slack-app.git
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
 
SLACK_EVENT_URL = 'events'  # same with default
SLACK_OAUTH_URL = 'oauth'  # same with default

SLACK_EVENTS = "my_slack_app.slack_events"
SLACK_SIGNING_SECRET = "SOMENICESECRETCODE"

```

```SLACK_OAUTH_URL``` and ```SLACK_OAUTH_URL``` in the above code are a same with default url. so, you can skip it. I just write it to show you the default URL explicitly.

3. add route to the django-slack-app
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    
    ...

    path('slack/', include("django_slack_app.urls")),
]

```
In this case, 
- Your event-subscription URL is "http://yourdomain/slack/events"
- Your OAuth redirect URL is  "http://yourdomain/slack/oauth" 


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

now, you can get slack events!


## FAQ
### What is the difference between this and others?
other libraries are:
- hard to use
- not integrated with Django
- includes unnecessary dependencies(like a flask)
- not support OAuth 
- or Developer have to manage the OAuth tokens
- NOT SUPPORT EVENT SUBSCRIPTION ** most important reason **
