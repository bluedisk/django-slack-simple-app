import hgtk
import slack

from django_slack_app import slack_events
from . import papago

SLACK_BOT_USER_TOKEN = "??"
client = slack.WebClient(token=SLACK_BOT_USER_TOKEN)


@slack_events.on("message")
def message_channels(event_data):
    event = event_data["event"]
    if "text" in event and "bot_id" not in event and "subtype" not in event:
        text = event["text"]

        if hgtk.checker.is_latin1(text):
            print("Translate %s characters to Korean" % len(text))
            translated = papago.translate(text, "en", "ko")
        else:
            print("Translate %s characters to English" % len(text))
            translated = papago.translate(text, "ko", "en")

        if translated:
            new_text = "%s\n> %s" % (text, translated.replace("\n", "\n> "))
            response = client.chat_update(
                channel=event["channel"], ts=event["ts"], text=new_text
            )
            assert response["ok"]
