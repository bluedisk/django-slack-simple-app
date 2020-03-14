from functools import lru_cache
from pyee import EventEmitter


@lru_cache(1)
def get_slack_events_adaptor():
    return EventEmitter()


slack_events = get_slack_events_adaptor()
