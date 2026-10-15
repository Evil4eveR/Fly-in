from __future__ import annotations

from typing import TYPE_CHECKING

from models.hub import Hub

if TYPE_CHECKING:
    from models.drone import Drone


class Connection:
    """A bidirectional link between two hubs, with a maximum number of drones that can traverse it at once."""  # noqa:E501
    def __init__(
            self,
            hub_a: Hub,
            hub_b: Hub,
            max_link_capacity: int = 1
            ) -> None:
        self.hub_a: Hub = hub_a
        self.hub_b: Hub = hub_b
        self.max_link_capacity: int = max_link_capacity
        # The list of drones currently traversing this connection
        self.drones: list[Drone] = []
