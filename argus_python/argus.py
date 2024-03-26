"""Main Argus module."""

import json
import socket
from typing import Dict, Optional

from event_bus import EventBus
from helpers import Helpers


class Argus:

    def __init__(
        self,
        username: Optional[str] = "",
        password: Optional[str] = "",
        host: Optional[str] = "127.0.0.1",
        port: Optional[int] = 1337,
    ) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_bus = EventBus()

    def send_authentication_data(self) -> None:
        connection_string = f"<ArgusAuth>{self.username}:{self.password}</ArgusAuth>"
        self.socket.send(connection_string.encode())

    def connect(self) -> None:
        try:
            self.socket.connect(
                (
                    self.host,
                    self.port,
                )
            )

            if self.username:
                self.send_authentication_data()

            while True:
                data = self.socket.recv(1024)
                if data:
                    data_str = data.decode("utf-8")

                    if Helpers.is_json_string(data_str):
                        self._publish_argus_data(data_str)
                    else:
                        print(f"Received: {data_str}")

        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")

        except EOFError:
            print("Connection closed by server")

        except Exception as err:
            print(f"Error receiving data: {str(err)}")

        finally:
            print("Socket closed")
            self._close_socket()

    def subscribe(self, subscriber: str, method_name: str) -> None:
        self.event_bus.subscribe(subscriber=subscriber, method_name=method_name)

    def _publish_argus_data(self, data: Dict[str, str]) -> None:
        argus_event = json.loads(data)
        self.event_bus.publish(argus_event)

    def _close_socket(self):
        if self.socket:
            self.socket.close()
