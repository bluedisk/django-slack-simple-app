from functools import lru_cache

from pyee import EventEmitter


@lru_cache(1)
def get_slack_events_adaptor() -> EventEmitter:
    return EventEmitter()


@lru_cache(1)
def get_slack_commands_adaptor() -> EventEmitter:
    return EventEmitter()


slack_events = get_slack_events_adaptor()
slack_commands = get_slack_commands_adaptor()
