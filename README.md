# pyding
PyDing is a (very) simple but effective event handler.


## Usage
---
```python
# Import the module
import pyding

# Attach a handler to an event.
@pyding.on("greetings")
def greeter(event):
    print("Hello there from pyding!")

# Call the event
pyding.call("greetings")

# Hello there from pyding!
```

### Cancellable events
You can also make events that can be cancelled, using the `cancellable` keyword for `pyding.call`
> ⚠️ - Cancelling and event which cannot be cancelled will raise `pyding.exceptions.UncancellableEvent`

```python
import pyding

# Attach the handler to an event
@pyding.on("check")
def checker(event):
    # Do stuff    
    # Cancel the event
    event.cancel()

# Call the event
event = pyding.call("check", cancellable=True)

event.cancelled
# will return True
```

### Hierarchy
Event handlers can have an priority attached to them. If the event is cancelled, it will not execute the next handlers. This behavior can be changed by the `blocking` keyword for `pyding.call`

```python
import pyding

# Attach the handler to an event
@pyding.on("check", priority=10)
def checker_one(event):
    print("I got executed!")


@pyding.on("check", priority=0)
def checker_two(event):
    print("Me too")


# Call the event
event = pyding.call("check")

# I got executed!
# Me too

```

```python
import pyding

# Attach the handler to an event
@pyding.on("check", priority=10)
def checker_one(event):
    print("I got executed!")
    event.cancel()


@pyding.on("check", priority=0)
def checker_two(event):
    # This won't be executed at first since it got cancelled by checker_one
    print("Me too")


# Call the event
pyding.call("check", cancellable=True)

# I got executed!

# Call the event and do not break if the event is cancelled.
event = pyding.call("check", cancellable=True, blocking=False)

# I got executed!
# Me too

event.cancelled
# True
```

### Dealing with the response
Events can return values, which will be attributed to `event.response`

```python
import pyding

# Attach the handler to an event
@pyding.on("greetings")
def greeter(event):
    return "Hello World!"


# Call the event
event = pyding.call("greetings")

event.response
# Hello World!
```

### Using arguments
Arguments can be passed onto the handlers through `pyding.call`

```python
import pyding

# Attach the handler to an event
@pyding.on("greetings")
def greeter(event, name):
    return f"Hello {name}!"


# Call the event
event = pyding.call("greetings", name="John Doe")

event.response
# Hello John Doe!
```