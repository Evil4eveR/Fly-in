from models.connection import Connection
from models.hub import Hub


class Map:
    """The network of hubs and connections."""

    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.start_hub: Hub | None = None
        self.end_hub: Hub | None = None
        self.hubs: dict[str, Hub] = {}
        self.connections: dict[tuple[str, str], Connection] = {}

    def add_hub(self, hub: Hub) -> None:
        """Register a hub by its name."""
        if hub.name in self.hubs:
            raise ValueError(f"Duplicate hub name: {hub.name!r}")
        self.hubs[hub.name] = hub

    def add_connection(self, conn: Connection) -> None:
        """Register a bidirectional connection, rejecting duplicates."""
        key = (min(conn.hub_a.name, conn.hub_b.name),
               max(conn.hub_a.name, conn.hub_b.name))
        if key in self.connections:
            raise ValueError(
                f"Duplicate connection: {key[0]}-{key[1]}"
                )
        self.connections[key] = conn

    def set_start(self, name: str) -> None:
        """Mark the named hub as the start hub."""
        if self.start_hub is not None:
            raise ValueError("Start hub already defined")

        if name not in self.hubs:
            raise ValueError(f"Unknown start hub: {name!r}")

        self.start_hub = self.hubs[name]

    def set_end(self, name: str) -> None:
        """Mark the named hub as the end hub."""
        if self.end_hub is not None:
            raise ValueError("End hub already defined")

        if name not in self.hubs:
            raise ValueError(f"Unknown end hub: {name!r}")

        self.end_hub = self.hubs[name]

    def get_connection(self, a: str, b: str) -> Connection | None:
        """Return the connection between two hubs, or None if absent."""
        key = (min(a, b),
               max(a, b))
        return self.connections.get(key)
