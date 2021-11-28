import json
from collections.abc import Iterable
from pprint import pprint

import requests
import slack
import slack.errors
from aiohttp.http_exceptions import HttpBadRequest
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, \
    HttpResponseBadRequest
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import slack_events, slack_commands
from .decorators import verify_slack_request
from .models import SlackUser, SlackTeam

if not isinstance(settings.SLACK_HANDLER, Iterable):
    __import__(settings.SLACK_HANDLER)

for handler in settings.SLACK_HANDLER:
    __import__(handler)

if not hasattr(settings, "SLACK_APP_TOKEN") or \
        not hasattr(settings, "SLACK_APP_BOT_TOKEN") or \
        not hasattr(settings, "SLACK_CLIENT_ID") or \
        not hasattr(settings, "SLACK_CLIENT_SECRET"):
    raise NotImplemented("You must enter the slack app settings")


class SlackCommandResponse:
    def __init__(self, url):
        self.url = url

    def ephemeral(self, text):
        payload = {"text": text, "response_type": "ephemeral"}
        return requests.post(self.url, json=payload)

    def in_channel(self, text):
        payload = {"text": text, "response_type": "in_channel"}
        return requests.post(self.url, json=payload)


@method_decorator(csrf_exempt, name='dispatch')
class SlackCommandView(View):

    @method_decorator(verify_slack_request)
    def post(self, request, *args, **kwargs):
        command = request.POST.get("command", "")
        event_data = request.POST.copy()

        slack_user = None
        try:
            slack_user = SlackUser.objects.get(id=event_data['user_id'])
            slack_user.update_info()
            event_data['user'] = slack_user
        except SlackUser.DoesNotExist:
            pass

        slack_commands.emit(command, event_data, slack_user, SlackCommandResponse(event_data['response_url']))

        # parsing and checking for the sub-command
        subcommand = request.POST.get("text", "").split()
        if subcommand:
            full_command = ".".join([command, subcommand[0].lower()])

            if slack_commands.listeners(full_command):
                slack_commands.emit(
                    full_command,
                    event_data, slack_user, SlackCommandResponse(event_data['response_url'])
                )

        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class SlackEventView(View):

    def get(self, request, *args, **kwargs):
        # If a GET request is made, return 404.
        return HttpResponseNotFound("It's working but not for you!")

    @method_decorator(verify_slack_request)
    def post(self, request, *args, **kwargs):
        """Slack Event View for handling Slack Event Call which was subscribed"""

        # Parse the request payload into JSON
        event_data = json.loads(request.body.decode('utf-8'))

        # Echo the URL verification challenge code back to Slack
        if "challenge" in event_data:
            return HttpResponse(event_data["challenge"])

        # Parse the Event payload and emit the event to the event listener
        if "event" in event_data:
            event = event_data['event']
            event_type = event["type"]

            slack_user = None
            if 'user' in event:
                try:
                    slack_user = SlackUser.objects.get(id=event['user'])
                    slack_user.set_default_channel(event['channel'])
                    slack_user.update_info()

                    event['user'] = slack_user
                except SlackUser.DoesNotExist:
                    pass

            print("Emmited: ", event_type)
            slack_events.emit(event_type, event_data, slack_user)
            return HttpResponse()

        return HttpResponseForbidden()


class SlackOAuthView(View):

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        if "code" not in request.GET:
            return HttpResponseBadRequest("Wrong code")

        payload = {
            "code": request.GET["code"],
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECRET
        }

        try:
            client = slack.WebClient()
            response = client.oauth_v2_access(**payload)
        except slack.errors.SlackApiError as e:
            return HttpResponseBadRequest("Invalid code")

        if not response["ok"]:
            print("E] processing failed...")
            pprint(response.data)
            return HttpResponse("failed")

        authed_user = response["authed_user"]
        team_info = response["team"]

        team, _ = SlackTeam.objects.update_or_create(
            id=team_info["id"],
            defaults={
                "name": team_info["name"]
            })
        team.update_info()

        if "access_token" in authed_user:
            user, _ = SlackUser.objects.update_or_create(
                id=authed_user["id"],
                defaults={
                    "token": authed_user["access_token"],
                    "team": team
                }
            )
            user.update_info()

            slack_events.emit("oauth", user)

        if hasattr(settings, "SLACK_AFTER_OAUTH") and settings.SLACK_AFTER_OAUTH:
            return HttpResponseRedirect(settings.SLACK_AFTER_OAUTH)

        return HttpResponseRedirect(reverse("oauth_done"))
