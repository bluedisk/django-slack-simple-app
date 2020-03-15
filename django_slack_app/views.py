import hashlib
import hmac
import json
from pprint import pprint
from time import time

import slack
from aiohttp.http_exceptions import HttpBadRequest
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from slack.errors import SlackApiError

from . import slack_events
from .models import SlackUserToken

__import__(settings.SLACK_EVENTS)

if not hasattr(settings, "SLACK_APP_TOKEN") or \
        not hasattr(settings, "SLACK_CLIENT_ID") or \
        not hasattr(settings, "SLACK_CLIENT_SECRET"):
    raise NotImplemented("You must enter the slack app settings")


class SlackEventView(View):
    """Slack Event View for handling Slack Event Call which was subscribed"""

    # If a GET request is made, return 404.
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound("It's working but not for you!")

    def post(self, request, *args, **kwargs):
        # Each request comes with request timestamp and request signature
        # emit an error if the timestamp is out of range
        req_timestamp = request.headers.get('X-Slack-Request-Timestamp')
        if abs(time() - int(req_timestamp)) > 60 * 5:
            slack_events.emit('error', 'Invalid request timestamp')
            return HttpResponseForbidden()

        # Verify the request signature using the app's signing secret
        # emit an error if the signature can't be verified
        req_signature = request.headers.get('X-Slack-Signature')
        if not self.verify_signature(request, req_timestamp, req_signature):
            slack_events.emit('error', 'Invalid request signature')
            return HttpResponseForbidden()

        # Parse the request payload into JSON
        event_data = json.loads(request.body.decode('utf-8'))

        # Echo the URL verification challenge code back to Slack
        if "challenge" in event_data:
            return HttpResponse(event_data["challenge"])

        # Parse the Event payload and emit the event to the event listener
        if "event" in event_data:
            event_type = event_data["event"]["type"]
            slack_events.emit(event_type, event_data)
            return HttpResponse()

        return HttpResponseForbidden()

    @staticmethod
    def verify_signature(request, timestamp, signature):
        # Verify the request signature of the request sent from Slack
        # Generate a new hash using the app's signing secret and request data

        req = str.encode('v0:' + str(timestamp) + ':') + request.body
        request_hash = 'v0=' + hmac.new(
            str.encode(settings.SLACK_SIGNING_SECRET),
            req, hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(request_hash, signature)


class SlackOAuthView(View):
    client = slack.WebClient()

    def get(self, request, *args, **kwargs):

        if "code" not in request.GET:
            raise HttpBadRequest("Wrong code")

        payload = {
            "code": request.GET["code"],
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECRET
        }

        try:
            response = self.client.oauth_v2_access(**payload)
        except SlackApiError as e:
            raise HttpBadRequest("Invalid code")

        if not response["ok"]:
            print("E] processing failed...")
            pprint(response.data)
            return HttpResponse("failed")

        authed_user = response["authed_user"]
        team = response["team"]

        token, _ = SlackUserToken.objects.update_or_create(
            user=authed_user["id"],
            defaults={
                "token": authed_user["access_token"],
                "team_id": team["id"],
                "team_name": team["name"],
            }
        )
        token.save()

        if hasattr(settings, "SLACK_AFTER_OAUTH") and settings.SLACK_AFTER_OAUTH:
            return HttpResponseRedirect(settings.SLACK_AFTER_OAUTH)

        return HttpResponseRedirect(reverse("oauth_done"))
