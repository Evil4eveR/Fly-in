from __future__ import annotations

from typing import TYPE_CHECKING

from models.zone_type import ZoneType

# This import ONLY runs during static type checking, NOT at runtime
if TYPE_CHECKING:
    from models.drone import Drone


class Hub:
    """A zone in the drone network. Tracks position, type, capacity, and current occupants."""  # noqa:E501
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str | None = None,
        max_drones: int = 1,
    ) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: ZoneType = zone_type
        self.color: str | None = color
        self.max_drones: int = max_drones
        self.drones: list[Drone] = []      # always empty at creation
