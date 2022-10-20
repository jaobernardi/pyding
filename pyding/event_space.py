import asyncio
from .structures import EventHandler, EventCall

class EventSpace:
    """
        Manages and holds the event listener/handlers.
    """
    def __init__(self, event_handler_class: EventHandler = None):
        self.event_handler_class = event_handler_class or EventHandler
        self.events = {}
    
    def register_handler(self, handler):
        if handler.event not in self.events:
            self.events[handler.event]: dict[str, dict[int, list[EventHandler]]] = {}
        
        # Check if the priority is already registered.
        if handler.priority not in self.events[handler.event]:
            self.events[handler.event][handler.priority] = []

        self.events[handler.event][handler.priority].append(handler)


    def get_handlers(self, event):
        # Get the ordered priorities
        index_order = list(self.events[event])
        index_order.sort(reverse=True) # Reverse the order to make it descending.


        # Index the handlers.
        handlers = []
        for index in index_order:
            for handler in self.events[event][index]:
                handlers.append(handler)
        return handlers


    def handler_registered(self, handler):
        return handler in self.events[handler.event][handler.priority] if handler.event in self.events else False

    def unregister_from_module(self, module):
        for event in self.events.values():
            for handlers in event.values():
                for handler in handlers:
                    if handler.origin_module == module:
                        handlers.remove(handler)

    def unregister_handler(self, handler):
        self.events[handler.event][handler.priority].remove(handler)


    # Define the "on" method
    def on(self, event_name: str, priority: int=0, register_ra: bool=True, function: bool=None, requirement_exceptions: bool=False, is_async: bool=None, **kwargs):
        """Attaches a handler

        Args:
            event_name (str): Event name
            priority (int, optional): Handler priority. Defaults to 0.
            register_ra (bool, optional): Register the handler rigth now. Defaults to True.
            function (bool, optional): Handler function

        Returns:
            EventHandler
        """
        # Wrap the function
        def wrapper(func):
            # Insert the handler function into the dict.
            handler = self.event_handler_class(func, event_name, priority, self, is_async=is_async, requirement_exceptions=requirement_exceptions, execution_requirements=kwargs)
            if register_ra:
                handler.register()
            return handler
        
        # If there isn't a function in the args, return the wrapper. 
        if not function:
            return wrapper
        
        # Run the wrapper function with the argument's function.
        wrapper(function)


    async def async_call(self, event_name: str, *args, **kwargs):
        """Calls an event with asynchronous handlers

        Args:
            event_name (str): Name of the event being called.

        Returns:
            EventCall
        """
        # Define the event call object.
        event_call = EventCall(event_name=event_name)
 
        # Return if there isn't an event registered with this name.
        if event_name not in self.events:
            return event_call

        # Run the handlers.
        calls = []
        for handler in self.get_handlers(event_name):
            handler: EventHandler
            handler_return = handler.async_call(event_call, args=args, kwargs=kwargs)
            if handler.is_async:
                calls.append(handler_return)
            else:
                event_call.responses.append(handler_return)
        event_call.responses = await asyncio.gather(*calls)
        # Return the event
        return event_call


    # Define the "call" method
    def call(self, event_name: str, cancellable: bool=False, blocking: bool=True, first_response: bool=False, *args, **kwargs):
        """Calls an event

        Args:
            event_name (str): Name of the event being called.
            cancellable (bool, optional): If the called event can be cancelled. Defaults to False.
            blocking (bool, optional): Stop the event if it has been cancelled. Defaults to True.
            first_response (bool, optional): Stop the event at the first response. Defaults to False.

        Returns:
            EventCall
        """
        
        # Define the event call object.
        event_call = EventCall(event_name=event_name, cancellable=cancellable)

        # Return if there isn't an event registered with this name.
        if event_name not in self.events:
            return event_call

        # Run the handlers.
        for handler in self.get_handlers(event_name):
            handler: EventHandler
            # Run the handler
            response = handler.call(event_call, args=args, kwargs=kwargs)
            event_call.responses.append(response)
            if response != None:
                # If this is the first response, break the loop
                if first_response:
                    break

            # If the event was cancelled, do not run the next handlers.
            if (event_call.cancelled and blocking) or event_call.stopped:
                break

        # Return the event
        return event_call

global_event_space = EventSpace()