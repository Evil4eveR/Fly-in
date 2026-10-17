from algorithms.pathfinder import Pathfinder
from models.drone import Drone
from models.hub import Hub
from models.map import Map


class Simulation:
    def __init__(self, world: Map) -> None:
        self.world = world
        self.drones: list[Drone] = []
        self.turn = 1
        
        assert world.nb_drones is not None
        assert world.start_hub is not None
        path = Pathfinder().findpath(self.world)
        for i in range(1, world.nb_drones + 1):
            drone = Drone(i, world.start_hub)
            drone.route = path
            self.drones.append(drone)
            world.start_hub.drones.append(drone)
    
    def run(self) -> None:
        while not all(drone.location == self.world.end_hub for drone in self.drones):
            moves = self._decide_moves()
            self._apply_moves(moves)
            self.turn += 1

    def _decide_moves(self) -> dict[int, Hub]:
        moves: dict[int, Hub] = {}
        
        # Sort drones so the ones furthest along the path move first.
        # This prevents a drone further back from taking a spot that a drone ahead of it needs.
        sorted_drones = sorted(self.drones, key=lambda d: d.route_index, reverse=True)
        
        # Keep a temporary copy of the drones in each hub
        current_hubs = {name: list(hub.drones) for name, hub in self.world.hubs.items()}

        # Temporary copy to count how many drones traverse each connection this turn
        current_conn_usage: dict[tuple[str, str], int] = {}

        for drone in sorted_drones:
            if drone.location == self.world.end_hub:
                continue
 
            next_index = drone.route_index + 1
            next_hub = drone.route[next_index]

            # Check Hub capacity
            hub_space = len(current_hubs[next_hub.name]) < next_hub.max_drones

            # Check if there is space in the destination
            if next_hub == self.world.end_hub:
                hub_space = True

            conn = self.world.get_connection(drone.location.name, next_hub.name)
            conn_space = True
            if conn is not None:
                conn_key = (min(conn.hub_a.name, conn.hub_b.name), 
                            max(conn.hub_a.name, conn.hub_b.name))
                current_on_conn = len(conn.drones)
                scheduled = current_conn_usage.get(conn_key, 0)
                if current_on_conn + scheduled >= conn.max_link_capacity:
                    conn_space = False
            if hub_space and conn_space:
                moves[drone.id] = next_hub

                # Update our temporary tracking: remove from old, add to new
                if drone in current_hubs[drone.location.name]:
                    current_hubs[drone.location.name].remove(drone)
                current_hubs[next_hub.name].append(drone)
                #Update connection tracking
                if conn is not None:
                    conn_key = (min(conn.hub_a.name, conn.hub_b.name), 
                                max(conn.hub_a.name, conn.hub_b.name))
                    current_conn_usage[conn_key] = current_conn_usage.get(conn_key, 0) + 1
        return moves

    def _apply_moves(self, moves: dict[int, Hub]) -> None:
        if not moves:
            return
        output_parts: list[str] = []
        for drone in self.drones:
            if drone.id in moves:
                drone.location.drones.remove(drone)
                drone.location = moves[drone.id]
                drone.route_index += 1
                drone.location.drones.append(drone)
                output_parts.append(f"D{drone.id}-{drone.location.name}")
        print(" ".join(output_parts))
