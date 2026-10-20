from algorithms.pathfinder import Pathfinder
from models.connection import Connection
from models.drone import Drone
from models.hub import Hub
from models.map import Map
from simulation.visualizer import Visualizer


class Simulation:
    def __init__(self, world: Map) -> None:
        self.world = world
        self.drones: list[Drone] = []
        self.turn = 1

        assert world.nb_drones is not None
        assert world.start_hub is not None
        paths = Pathfinder().find_multiple_paths(self.world)
        for i in range(1, world.nb_drones + 1):
            drone = Drone(i, world.start_hub)
            assigned_path = paths[(i - 1) % len(paths)]
            drone.route = assigned_path
            self.drones.append(drone)
            world.start_hub.drones.append(drone)

    def run(self) -> None:
        while not all(drone.location == self.world.end_hub for drone in self.drones):  # noqa:E501
            moves = self._decide_moves()
            if not moves:
                raise RuntimeError("Deadlock detected! Drones are stuck.")
            self._apply_moves(moves)
            self.turn += 1

    def _decide_moves(self) -> dict[int, Hub | Connection]:
        moves: dict[int, Hub | Connection] = {}

        # Drones further along the route get priority.
        sorted_drones = sorted(
            self.drones,
            key=lambda d: d.route_index,
            reverse=True,
        )

        # Temporary lists to track available space in each hub.
        current_hubs = {
            name: list(hub.drones)
            for name, hub in self.world.hubs.items()
        }

        # Start with the actual number of drones on each connection.
        # Update this count as moves are planned.
        current_conn_load = {
            self._connection_key(conn): len(conn.drones)
            for conn in self.world.connections.values()
        }

        for drone in sorted_drones:

            # This drone has already arrived.
            if drone.location == self.world.end_hub:
                continue

            # Find the next step in this drone's route.
            next_index = drone.route_index + 1

            if next_index >= len(drone.route):
                continue

            curr_location = drone.location
            next_step = drone.route[next_index]

            # CASE 1: The next step is a Hub.
            if isinstance(next_step, Hub):

                # Check whether the destination has space.
                # The end hub is exempt from the capacity limit,
                # matching your original code.
                if next_step != self.world.end_hub:
                    if len(current_hubs[next_step.name]) >= next_step.max_drones:  # noqa:E501
                        continue

                # CASE 1A: Hub -> Hub
                if isinstance(curr_location, Hub):

                    conn = self.world.get_connection(
                        curr_location.name,
                        next_step.name,
                    )

                    # These hubs must be connected.
                    if conn is None:
                        continue

                    key = self._connection_key(conn)

                    # Is there enough capacity on this connection?
                    if current_conn_load[key] >= conn.max_link_capacity:
                        continue

                    # Reserve capacity for this move.
                    current_conn_load[key] += 1

                # CASE 1B: Connection -> Hub
                elif isinstance(curr_location, Connection):

                    # Make sure the destination belongs to this connection.
                    if next_step.name not in (
                        curr_location.hub_a.name,
                        curr_location.hub_b.name,
                    ):
                        continue

                    # The drone is leaving the connection,
                    # so one space will become available.
                    key = self._connection_key(curr_location)
                    current_conn_load[key] -= 1

                else:
                    continue

            # CASE 2: The next step is a Connection.
            elif isinstance(next_step, Connection):

                # A drone can enter a connection from a Hub.
                if not isinstance(curr_location, Hub):
                    continue

                # Make sure the current hub belongs to this connection.
                if curr_location.name not in (
                    next_step.hub_a.name,
                    next_step.hub_b.name,
                ):
                    continue

                key = self._connection_key(next_step)

                # Is there enough capacity to enter the connection?
                if current_conn_load[key] >= next_step.max_link_capacity:
                    continue

                # Reserve one space on the connection.
                current_conn_load[key] += 1

            else:
                continue

            # The move has passed all checks.
            moves[drone.id] = next_step

            # Update the temporary hub lists.
            # The real drone locations are changed later by _apply_moves().
            if isinstance(curr_location, Hub):
                current_hubs[curr_location.name].remove(drone)

            if isinstance(next_step, Hub):
                current_hubs[next_step.name].append(drone)

        return moves

    @staticmethod
    def _connection_key(conn: Connection) -> tuple[str, str]:
        first = min(conn.hub_a.name, conn.hub_b.name)
        second = max(conn.hub_a.name, conn.hub_b.name)
        return first, second

    def _apply_moves(self, moves: dict[int, Hub | Connection]) -> None:
        if not moves:
            return
        output_parts: list[str] = []
        for drone in self.drones:
            if drone.id in moves:
                drone.location.drones.remove(drone)
                drone.location = moves[drone.id]
                drone.route_index += 1
                drone.location.drones.append(drone)
                if isinstance(drone.location, Connection):
                    output_parts.append(f"D{drone.id}-{drone.location.hub_a.name}-{drone.location.hub_b.name}")  # noqa:E501
                else:
                    colored_name = Visualizer.colorize(drone.location.name, drone.location.color)  # noqa:E501
                    output_parts.append(f"D{drone.id}-{colored_name}")
        print(" ".join(output_parts))
