from .methods import on, call, async_call, handlers_registered, register_handler, unregister_from_module, unregister_handler
from .structures import EventCall, EventHandler, EventSupport
from .exceptions import UncancellableEvent
from .event_space import EventSpace

__name__ = "pyding"
__version__ = "1.6.1"