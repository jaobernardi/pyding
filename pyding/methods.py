# methods.py
from .event_space import global_event_space
from .structures import EventCall, EventHandler


on = global_event_space.on
call = global_event_space.call
async_call = global_event_space.async_call
handlers_registered = global_event_space.handler_registered
register_handler = global_event_space.register_handler
unregister_from_module = global_event_space.unregister_from_module
unregister_handler = global_event_space.unregister_handler
get_handlers = global_event_space.get_handlers
