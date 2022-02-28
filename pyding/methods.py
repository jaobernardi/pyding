# methods.py
from .event_space import global_event_space
from .structures import EventCall, EventHandler
import asyncio


# Define the "on" method
def on(*args, **kwargs):
    return global_event_space.on(*args, **kwargs)


# Define the "call" method
def call(*args, **kwargs):
    return global_event_space.call(*args, **kwargs)
