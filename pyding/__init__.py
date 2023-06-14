from .methods import wait_for, on, call, async_call, handlers_registered, register_handler, unregister_from_module, unregister_handler, get_handlers
from .structures import EventCall, EventHandler, EventSupport
from .exceptions import UncancellableEvent
from .event_space import EventSpace

__name__ = "pyding"
__version__ = "1.7.1"