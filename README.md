<h1 align="center"> pyding 🛎 </h1>
<p align="center">PyDing is a (very) simple but effective event handler.</p>
<p align="center">
    <a href="https://twitter.com/jaobernard">
        <img alt="Feito por João Bernardi" src="https://img.shields.io/badge/feito%20por-%40jaobernard-39013C">
    </a>
    <a>
        <img src="https://img.shields.io/github/last-commit/jaobernardi/pyding?color=39013C">
    </a>
    <a href="https://pypi.org/project/pyding">
        <img src="https://img.shields.io/pypi/dm/pyding?color=39013C">
    </a>
</p>

<br>
<br>

<h2 align="center"> Usage </h2>

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

<h3 align="center"> Async handlers </h2>


```python
# Import the module
import pyding
import asyncio

# Attach a handler to an event.
@pyding.on("greetings", is_async=True)
async def greeter(event):
    print("Hello there from pyding!")

# Call the event
asyncio.run(pyding.async_call('greetings'))

# Hello there from pyding!
```

<h3 align="center"> Cancellable events </h3>

<p align="center"> You can also make events that can be cancelled, using the <code>cancellable</code> keyword for <code>pyding.call</code></p>

> ⚠️ - Cancelling an event which cannot be cancelled will raise `pyding.exceptions.UncancellableEvent`

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

<h3 align="center"> Hierarchy </h3>

<p align="center"> Event handlers can have an priority attached to them. If the event is cancelled, it will not execute the next handlers. This behavior can be changed by the <code>blocking</code> keyword for <code>pyding.call</code></p>

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
> 🛑 - You can also stop the event execution by using `event.stop()`

<h3 align="center">  Dealing with the response </h3>

<p align="center"> Events can return values, which will be attributed to <code>event.response</code> and <code>event.responses</code></p>

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

event.responses
# ['Hello World!']
```

<h3 align="center">  Using arguments </h3>

<p align="center"> Arguments can be passed onto the handlers through <code>pyding.call</code> </p>

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

<p align="center"> Essential arguments can be passed to <code>@pyding.on</code> to make sure the handler only will be called if they're met.</p>

```python
import pyding

# Attach the handler to an event
@pyding.on("greetings", name="John Doe")
def john_doe_greeter(event, name, time):
    return f"Hello {name}! It's currently {time}"


# Call the event
event_two = pyding.call("greetings", name="John Bar", time="10 AM")
# There won't be any response since the handler won't be called since the 'name' essential keyword wasn't equal to 'John Doe'.
event_two.response
# None

# Call the event
event = pyding.call("greetings", name="John Doe", time="10 AM")

event.response
# "Hello John Doe! It's currently 10 AM"

# You can also raise pyding.exceptions.UnfulfilledException if you add requirement_exceptions=True to pyding.on decorator.
```

<h3 align="center"> Events within classes </h3>
<p align="center"> Objects can have methods that act as an event handler. </p>

```python
import pyding


class MyClass(pyding.EventSupport):
    def __init__(self, name):
        self.register_events()
        self.name = name

    @pyding.on("my_event")
    def event_handler(self, event):
        print(f"Hello World from MyClass! My name is {self.name}.")

# Nothing will happen because there is no instance of MyClass
pyding.call("my_event")

myclass = MyClass("foo")

pyding.call("my_event")
# "Hello world from MyClass! My name is foo."
```

<h3 align="center"> Dealing with Event Spaces </h3>
<p align="center"> Event spaces allow to separate event handlers. </p>

```python
# Import the module
import pyding

# Create an Event Space
myspace = pyding.EventSpace()

# Attach a handler to an event.
@myspace.on("greetings")
def greeter(event):
    print("Hello there from myspace's event space!")

# Calling the event from the global space won't trigger any handler from myspace.
pyding.call("greetings")

# Calling the event from myspace will trigger the "greeter" handler.
myspace.call("greetings")
# Hello there from myspace's event space!
```

<h3 align="center"> Removing handlers </h3>
<p align="center"> Event spaces allow you to unregister handlers. </p>

```python
# Import the module
import pyding

# Attach a handler to an event.
@on("greetings")
def greeter(event):
    print("Hello there from myspace's event space!")

# Unregister event
pyding.unregister_handler(greeter)
# Or
greeter.unregister()
# You can also remove handlers from other modules by using pyding.unregister_from_module(module)

```

