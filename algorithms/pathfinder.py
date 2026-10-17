from models.hub import Hub
from models.map import Map
from models.zone_type import ZoneType


class Pathfinder:
    def get_neighbors(self, world: Map, hub_name: str) -> list[str]:
        """Return the names of all neighboring hubs connected to the given hub."""
        neighbors: list[str] = []
        for key in world.connections:
            if hub_name in key:
                if hub_name == key[0]:
                    neighbors.append(key[1])
                else:
                    neighbors.append(key[0])
        return neighbors

    def get_cost(self, world: Map, hub_name: str) -> float:
        """Return the travel cost of entering a hub based on its zone type."""
        if world.hubs[hub_name].zone_type == ZoneType.BLOCKED:
            return float('inf')
        elif world.hubs[hub_name].zone_type == ZoneType.RESTRICTED:
            return 2.0
        else:
            return 1.0

    def findpath(self, world: Map) -> list[Hub]:
        """Find the lowest-cost path from the start hub to the end hub using Dijkstra's algorithm."""
        assert world.start_hub is not None
        assert world.end_hub is not None

        distances: dict[str, float] = {name: float('inf') for name in world.hubs}  # noqa:501
        distances[world.start_hub.name] = 0.0

        previous: dict[str, str | None] = {name: None for name in world.hubs}
        univisited = set(world.hubs)

        while univisited:
            curr_name = min(univisited, key=lambda name: distances[name])

            if curr_name == world.end_hub.name:
                break

            univisited.remove(curr_name)
            neighbors = self.get_neighbors(world, curr_name)

            for nei in neighbors:
                cost = self.get_cost(world, nei)

                if cost == float('inf'):
                    continue

                new_distance = distances[curr_name] + cost

                if new_distance < distances[nei]:
                    distances[nei] = new_distance
                    previous[nei] = curr_name

        path: list[Hub] = []
        current_name: str | None = world.end_hub.name

        while current_name is not None:
            path.append(world.hubs[current_name])
            current_name = previous[current_name]

        # We built it backwards, so reverse it
        path.reverse()
        return path
