from models.connection import Connection
from models.hub import Hub
from models.map import Map
from models.zone_type import ZoneType


class Parser:
    def __init__(self) -> None:
        ...

    def _parse_metadata(self, raw: str) -> dict[str, str]:
        """Parse metadata such as 'color=blue max_drones=2'."""
        metadata: dict[str, str] = {}
        for item in raw.split():
            if "=" not in item:
                raise ValueError(f"Malformed metadata item: {item!r}")

            key, value = item.split("=", 1)

            if not key or not value:
                raise ValueError(f"Malformed metadata item: {item!r}")

            if key in metadata:
                raise ValueError(f"Duplicate metadata key: {key!r}")

            metadata[key] = value

        return metadata

    def _parse_nb_drones(self, line: str) -> int:
        """ Parse drone numbes with validation """
        key, value = line.strip().split(":", 1)
        if key.strip() != "nb_drones":
            raise IndexError("Expected 'nb_drones'")
        try:
            nb = int(value.strip())
        except ValueError:
            raise ValueError("Drones numbers must be an integer") from None
        if nb <= 0:
            raise ValueError("Drones number must be positive")
        return nb

    def _parse_hub_line(self, line: str, world: Map) -> None:
        """Parse a hub/start_hub/end_hub line and register the hub in the map."""  # noqa:E501

        # Separate the header from optional metadata
        if "[" in line:
            head, raw_metadata = line.split("[", 1)

            if "]" not in raw_metadata:
                raise ValueError("Missing closing bracket")

            raw_metadata, rest = raw_metadata.split("]", 1)

            if rest.strip():
                raise ValueError("Unexpected content after metadata")
        else:
            head = line
            raw_metadata = ""
        # Parse record type and hub information
        record_type, data = head.split(":", 1)
        record_type = record_type.strip()

        if record_type not in {"hub", "start_hub", "end_hub"}:
            raise ValueError(f"Unknown hub type: {record_type!r}")

        parts = data.split()

        if len(parts) != 3:
            raise ValueError("A hub must have a name and two coordinates")

        name = parts[0]
        x = int(parts[1])
        y = int(parts[2])
        # Parse metadata
        metadata = self._parse_metadata(raw_metadata)

        allowed_keys = {"color", "zone", "max_drones"}
        unknown_keys = metadata.keys() - allowed_keys

        if unknown_keys:
            raise ValueError(f"Unknown hub metadata: {unknown_keys}")

        max_drones_str = metadata.get("max_drones")
        if max_drones_str is None:
            max_drones = 1
        else:
            try:
                max_drones = int(max_drones_str)
            except ValueError:
                raise ValueError(
                    f"Invalid max_drones: {max_drones_str!r}"
                ) from None

            if max_drones <= 0:
                raise ValueError("max_drones must be positive")

        hub = Hub(name, x, y)
        hub.color = metadata.get("color")
        zone = metadata.get("zone", "normal")
        hub.zone_type = ZoneType(zone)
        hub.max_drones = max_drones
        world.add_hub(hub)

        if record_type == "start_hub":
            world.set_start(hub.name)
        elif record_type == "end_hub":
            world.set_end(hub.name)

    def _parse_connection_line(self, line: str, world: Map) -> None:
        """Parse a connection and add it to the map."""
        if "[" in line:
            head, raw_metadata = line.split("[", 1)

            if "]" not in raw_metadata:
                raise ValueError("Missing closing bracket")

            raw_metadata, rest = raw_metadata.split("]", 1)

            if rest.strip():
                raise ValueError("Unexpected content after metadata")
        else:
            head = line
            raw_metadata = ""
        # Parse record type and connection information
        conn, data = head.split(":", 1)
        # Validate the record type
        if conn.strip() != "connection":
            raise ValueError(f"Invalid connection type: {conn!r}")
        # Parse the hub names
        parts = data.strip().split("-")

        if len(parts) != 2:
            raise ValueError(f"Invalid connection format: {data!r}")

        hub_a_name, hub_b_name = (part.strip() for part in parts)
        # Resolve hub names to Hub objects
        if hub_a_name not in world.hubs:
            raise ValueError(f"Unknown hub: {hub_a_name!r}")

        if hub_b_name not in world.hubs:
            raise ValueError(f"Unknown hub: {hub_b_name!r}")

        hub_a = world.hubs[hub_a_name]
        hub_b = world.hubs[hub_b_name]
        metadata = self._parse_metadata(raw_metadata)

        capacity_str = metadata.get("max_link_capacity")
        if capacity_str is None:
            capacity = 1
        else:
            try:
                capacity = int(capacity_str)
            except ValueError:
                raise ValueError(
                    f"Invalid max_link_capacity: {capacity_str!r}"
                ) from None

            if capacity <= 0:
                raise ValueError("max_link_capacity must be positive")

        connection = Connection(hub_a, hub_b, capacity)
        world.add_connection(connection)

    def parse(self, filepath: str) -> Map:
        world = Map()
        with open(filepath, "r") as f:
            for line_number, raw_line in enumerate(f, start=1):
                raw_line = raw_line.split("#", 1)[0].strip()
                if not raw_line:
                    continue
                try:
                    if raw_line.startswith("nb_drones"):
                        world.nb_drones = self._parse_nb_drones(raw_line)
                    elif raw_line.startswith("connection"):
                        self._parse_connection_line(raw_line, world)
                    else:
                        self._parse_hub_line(raw_line, world)
                except ValueError as e:
                    raise ValueError(f"Line {line_number}: {e}") from e
        if not world.nb_drones or world.nb_drones < 1:
            raise ValueError("the drones number is missing in the map")
        if not world.start_hub:
            raise ValueError("the start hub is missing")
        if not world.end_hub:
            raise ValueError("the end hub is missing")
        return world
