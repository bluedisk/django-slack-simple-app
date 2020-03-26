import hashlib
import hmac
import json
from time import time

from django.conf import settings
from django.core.exceptions import PermissionDenied

from . import slack_events


def verify_slack_request(function):
    def wrap(request, *args, **kwargs):
        # Each request comes with request timestamp and request signature
        # emit an error if the timestamp is out of range
        req_timestamp = request.headers.get('X-Slack-Request-Timestamp') or 0
        if abs(time() - int(req_timestamp)) > 60 * 5:
            slack_events.emit('error', 'Invalid request timestamp')
            return PermissionDenied

        # Verify the request signature using the app's signing secret
        # emit an error if the signature can't be verified
        req_signature = request.headers.get('X-Slack-Signature')
        if not verify_slack_signature(request, req_timestamp, req_signature):
            slack_events.emit('error', 'Invalid request signature')
            return PermissionDenied

        return function(request, *args, **kwargs)

    # wrap.__doc__ = function.__doc__
    # wrap.__name__ = function.__name__
    return wrap


def verify_slack_signature(request, timestamp, signature):
    # Verify the request signature of the request sent from Slack
    # Generate a new hash using the app's signing secret and request data

    req = str.encode('v0:' + str(timestamp) + ':') + request.body
    request_hash = 'v0=' + hmac.new(
        str.encode(settings.SLACK_SIGNING_SECRET),
        req, hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(request_hash, signature)