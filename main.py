import sys

from parsing.parser import Parser
from algorithms.pathfinder import Pathfinder

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
    pathfinder = Pathfinder()
    path = pathfinder.findpath(world)

    print("Path found:")
    print(" -> ".join([hub.name for hub in path]))

if __name__ == "__main__":
    main()
