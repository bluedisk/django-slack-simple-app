# django-slack-app

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