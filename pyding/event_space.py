from .structures import EventHandler, EventCall

class EventSpace:
    def __init__(self):
        self.events = {}
    
    def register_handler(self, handler):
        if handler.event not in self.events:
            self.events[handler.event] = {}
        
        # Check if the priority is already registered.
        if handler.priority not in self.events[handler.event]:
            self.events[handler.event][handler.priority] = []

        self.events[handler.event][handler.priority].append(handler)


    def unregister_handler(self, handler):
        self.events[handler.event][handler.priority].remove(handler)

    # Define the "on" method
    def on(self, event_name, priority=0, register_ra=True, function=None):
        # Wrap the function
        def wrapper(func):
            # Insert the handler function into the dict.
            handler = EventHandler(func, event_name, priority, self)
            if register_ra:
                handler.register()
            return handler
        
        # If there isn't a function in the args, return the wrapper. 
        if not function:
            return wrapper
        
        # Run the wrapper function with the argument's function.
        wrapper(function)


    # Define the "call" method
    def call(self, event_name, cancellable=False, blocking=True, first_response=False, *args, **kwargs):
        # Return nothing if there isn't an event registered with this name.
        if event_name not in self.events:
            return
        
        # Define the event call object.
        event_call = EventCall(event_name=event_name, cancellable=cancellable)

        # Get the ordered priorities
        index_order = list(self.events[event_name])
        index_order.sort(reverse=True) # Reverse the order to make it descending.


        # Run the handlers.
        for index in index_order:
            for handler in self.events[event_name][index]:
                # Run the handler
                response = handler.call(event_call, args=args, kwargs=kwargs)            
                event_call.response = response

                # If this is the first response, break the loop
                if response and first_response:
                    return event_call

                # If the event was cancelled, do not run the next handlers.
                if event_call.cancelled and blocking:
                    break

        # Return the event
        return event_call

global_event_space = EventSpace()