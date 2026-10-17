from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.connection import Connection
    from models.hub import Hub


class Drone:
    """A drone in the network. Tracks its ID, current location, and planned route."""  # noqa:E501

    def __init__(self, drone_id: int, location: Hub | Connection) -> None:
        self.id: int = drone_id
        self.location: Hub | Connection = location
        # The planned route for the drone, can be empty if no route is set
        self.route: list[Hub | Connection] = []
        # The index of the next hub or connection in the route that the drone is moving towards # noqa:E501
        self.route_index: int = 0
