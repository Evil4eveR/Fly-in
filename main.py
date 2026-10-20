import sys

from algorithms.pathfinder import Pathfinder
from models.hub import Hub
from parsing.parser import Parser
from simulation.simulation import Simulation


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <map_file>")
        sys.exit(1)
    try:
        world = Parser().parse(sys.argv[1])
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    print(f"Loaded map: {len(world.hubs)} hubs, "
          f"{len(world.connections)} connections, "
          f"{world.nb_drones} drones")

    paths = Pathfinder().find_multiple_paths(world)
    print(f"Found {len(paths)} path(s):")
    for i, path in enumerate(paths):
        path_str = " -> ".join([
            h.name if isinstance(h, Hub) else f"{h.hub_a.name}-{h.hub_b.name}"
            for h in path
        ])
        print(f"Path {i+1}: {path_str}")
    # ... after parsing ...
    try:
        sim = Simulation(world)
        sim.run()
    except (RuntimeError) as e:
        print(e)


if __name__ == "__main__":
    main()
