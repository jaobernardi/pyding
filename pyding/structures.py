#structures.py
from .exceptions import UncancellableEvent

# Define the EventCall class
class EventCall:
    def __init__(self, event_name, cancellable=False):
        self.__name = event_name
        self.__cancelled = False
        self.cancellable = cancellable        
        self.response = None
    
    # Cancelling is only one-way. 
    def cancel(self):
        if self.cancellable:
            self.__cancelled = True
            return
        raise UncancellableEvent(f'{self.event_name} is not an cancellable event.')
    
    # Using it as a property since we don't want it to be writable 
    @property
    def cancelled(self):
        return self.__cancelled

    @property
    def name(self):
        return self.__name
    
    def __repr__(self):
        return f'<EventCall _name={repr(self.name)} _cancelled={self.cancelled} _response={repr(self.response)}>'