# methods.py
from .structures import EventCall

#Store the event handlers
events = {}

# Define the "on" method
def on(event_name, priority=0, function=None):
    # Check if the event is in the events dictionary.
    if event_name not in events:
        events[event_name] = {}
    
    # Check if the priority is already registered.
    if priority not in events[event_name]:
        events[event_name][priority] = []

    # Wrap the function
    def wrapper(func):
        # Insert the handler function into the dict.
        events[event_name][priority].append(func)
    
    # If there isn't a function in the args, return the wrapper. 
    if not function:
        return wrapper
    
    # Run the wrapper function with the argument's function.
    wrapper(function)


# Define the "call" method
def call(event_name, cancellable=False, blocking=True, *args, **kwargs):
    # Return nothing if there isn't an event registered with this name.
    if event_name not in events:
        return
    
    # Define the event call object.
    event_call = EventCall(event_name=event_name, cancellable=cancellable)

    # Get the ordered priorities
    index_order = list(events[event_name])
    index_order.sort(reverse=True) # Reverse the order to make it descending.


    # Run the handlers.
    for index in index_order:
        for handler in events[event_name][index]:
            # Run the handler
            event_call.response = handler(event_call, *args, **kwargs)

            # If the event was cancelled, do not run the next handlers.
            if event_call.cancelled and blocking:
                break

    # Return the event
    return event_call