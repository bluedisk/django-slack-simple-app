import json
from pprint import pprint

import slack
import slack.errors

from aiohttp.http_exceptions import HttpBadRequest
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import slack_events, slack_commands
from .decorators import verify_slack_request
from .models import SlackUser


__import__(settings.SLACK_EVENTS)

USER_MODEL = SlackUser
if hasattr(settings, "SLACK_USER_MODEL"):
    USER_MODEL = import_string(settings.SLACK_USER_MODEL)

if not hasattr(settings, "SLACK_APP_TOKEN") or \
        not hasattr(settings, "SLACK_CLIENT_ID") or \
        not hasattr(settings, "SLACK_CLIENT_SECRET"):
    raise NotImplemented("You must enter the slack app settings")


@method_decorator(csrf_exempt, name='dispatch')
class SlackCommandView(View):

    @method_decorator(verify_slack_request)
    def post(self, request, *args, **kwargs):
        command = request.POST.get("command", "")
        event_data = request.POST.copy()

        try:
            token = USER_MODEL.objects.get(user=event_data['user_id'])
            client = slack.WebClient(token=token.token)

            event_data['user'] = token
            event_data['client'] = client
        except USER_MODEL.DoesNotExist:
            pass

        slack_commands.emit(command, event_data)

        # parsing and checking for the sub-command
        subcommand = request.POST.get("text", "").split()[0].lower()
        if subcommand:
            full_command = ".".join([command, subcommand])

            if slack_commands.listeners(full_command):
                slack_commands.emit(full_command, event_data)

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

            if 'user' in event:
                try:
                    token = USER_MODEL.objects.get(user=event['user'])
                    client = slack.WebClient(token=token.token)

                    event['user'] = token
                    event['client'] = client
                except USER_MODEL.DoesNotExist:
                    pass

            slack_events.emit(event_type, event_data)
            return HttpResponse()

        return HttpResponseForbidden()


class SlackOAuthView(View):

    def get(self, request, *args, **kwargs):
        if "code" not in request.GET:
            raise HttpBadRequest("Wrong code")

        payload = {
            "code": request.GET["code"],
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECRET
        }

        try:
            client = slack.WebClient()
            response = client.oauth_v2_access(**payload)
        except slack.errors.SlackApiError as e:
            raise HttpBadRequest("Invalid code")

        if not response["ok"]:
            print("E] processing failed...")
            pprint(response.data)
            return HttpResponse("failed")

        authed_user = response["authed_user"]
        team = response["team"]

        token, _ = USER_MODEL.objects.update_or_create(
            user=authed_user["id"],
            defaults={
                "token": authed_user["access_token"],
                "team_id": team["id"],
                "team_name": team["name"],
            }
        )
        slack_events.emit("oauth", token)

        if hasattr(settings, "SLACK_AFTER_OAUTH") and settings.SLACK_AFTER_OAUTH:
            return HttpResponseRedirect(settings.SLACK_AFTER_OAUTH)

        return HttpResponseRedirect(reverse("oauth_done"))
