# ARGUS Python Client

This is the official Python library for the ARGUS Engine, this library helps Python developers and applications seamlessly integrate to the ARGUS Engine, authentication and event listening.

## Install via pip

```sh
pip install argus-python
```

Usage -

```py
from argus import Argus
```

Have a class to define the function to be called when you receive an Argus Event

```py
class Testsub:
    def on_event(self, argus_event: Dict[str, str]) -> None:
        print(argus_event.get("Action"))
        print(argus_event.get("ActionDescription"))
        print(argus_event.get("Name"))
        print(argus_event.get("Timestamp"))
```

Finally use argus like this

```py
subscriber = Testsub()

argus = Argus()  # Optionally you can pass the host and port, and auth credentials inclusive.

argus.subscribe(subscriber, "on_event")
argus.connect()
```

You can also set a timeout for how long you wish to wait for data

```py
argus.connect(timeout=60)
```
