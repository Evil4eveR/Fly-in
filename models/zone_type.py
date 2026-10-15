from enum import Enum


class ZoneType(Enum):
    """Types of zones in the drone network, each with a distinct movement cost or restriction."""  # noqa:E501
    NORMAL = 'normal'
    BLOCKED = 'blocked'
    RESTRICTED = 'restricted'
    PRIORITY = 'priority'
