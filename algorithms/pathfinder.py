from models.connection import Connection
from models.hub import Hub
from models.map import Map
from models.zone_type import ZoneType


class Pathfinder:
    def get_neighbors(self, world: Map, hub_name: str) -> list[str]:
        """Return the names of all neighboring hubs connected to the given hub."""  # noqa:E501
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

    def findpath(self, world: Map, penalized_hubs: set[str] | None = None) -> list[Hub | Connection]:  # noqa:E501
        """Find the lowest-cost path from the start hub to the end hub using Dijkstra's algorithm."""  # noqa:E501
        assert world.start_hub is not None
        assert world.end_hub is not None
        if penalized_hubs is None:
            penalized_hubs = set()
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
                if nei in penalized_hubs:
                    cost += 10.0  # heavy penalty to force different route

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

        # built it backwards, so reverse it
        path.reverse()
        final_route: list[Hub | Connection] = []
        for i in range(len(path)):
            curr_hub = path[i]
            if i > 0:
                prev_hub = path[1 - i]
                if curr_hub.zone_type == ZoneType.RESTRICTED:
                    conn = world.get_connection(prev_hub.name, curr_hub.name)
                    if conn:
                        final_route.append(conn)
            final_route.append(curr_hub)
        return final_route

    def find_multiple_paths(self, world: Map, max_paths: int = 2) -> list[list[Hub | Connection]]:  # noqa:E501
        """Finds up to max_paths unique paths by penalizing used hubs."""
        paths: list[list[Hub | Connection]] = []
        penalized: set[str] = set()

        for _ in range(max_paths):
            path = self.findpath(world, penalized)
            if not path:
                break

            # check if this is a duplicate of a path already found
            if path not in paths:
                paths.append(path)
            # Penalize all intermediate hubs so the next search finds a different route  # noqa:E501
            for node in path:
                if isinstance(node, Hub) and node != world.start_hub and node != world.end_hub:  # noqa:E501
                    penalized.add(node.name)
        if not paths:
            return [self.findpath(world)]
        return paths
