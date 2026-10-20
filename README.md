*This project has been created as part of the 42 curriculum by ymarmoud.*

# Fly-in: Drone Routing System

## Description

**Fly-in** is an object-oriented Python simulation designed to route a fleet of autonomous drones from a starting hub to an ending hub through a network of connected zones. The goal of the project is to navigate dynamic constraints, including zone capacities (`max_drones`), connection capacities (`max_link_capacity`), and variable movement costs (e.g., restricted zones). The program parses a text-based map, finds optimal paths, and simulates the turn-by-turn movement of all drones simultaneously, ensuring no collisions or capacity violations occur.

## Instructions

### Requirements

- Python 3.10 or later
- `flake8` and `mypy` for linting

### Installation

Clone the repository and install the dependencies using the provided `Makefile`:

    make install

### Execution

Run the simulation by passing a map file as an argument:

    make run FILE=maps/easy/02_simple_fork.txt

Or directly via Python:

    python3 main.py maps/easy/02_simple_fork.txt

### Makefile Rules

- `make install`: Sets up the environment and installs dependencies.
- `make run FILE=<path>`: Executes the simulation.
- `make debug FILE=<path>`: Runs the simulation using `pdb`.
- `make lint`: Runs `flake8` and `mypy` with strict flags.
- `make clean`: Removes `__pycache__` and `.mypy_cache`.

## Algorithm & Implementation Strategy

The project is divided into three distinct phases:

### 1. Parsing & Object Modeling
The parser reads the map line by line, validating syntax, extracting metadata (colors, capacities, zone types), and building a graph of `Hub` and `Connection` objects. `ZoneType` is strictly enforced using an Enum to prevent invalid states.

### 2. Pathfinding (Dijkstra's Algorithm)
Because zones have different movement costs (normal = 1, priority = 1, restricted = 2, blocked = infinity), a standard BFS is insufficient. We use Dijkstra's Algorithm to find the path with the lowest total turn cost.
- For restricted zones, the pathfinder inserts the `Connection` object into the route. This forces the simulation to spend a turn in transit, respecting the rule that a drone cannot wait on a connection.

### 3. Simulation (Simultaneous Movement)
The simulation engine operates in discrete turns using a two-phase approach (Decide, then Apply):
- **Decide Phase:** To handle the "revolving door" rule (where a drone leaving a hub frees space for a drone entering that same turn), we calculate the projected occupancy. Drones are processed by `route_index` (furthest along the path first) to prevent bottlenecks. We validate both the destination hub's `max_drones` and the connection's `max_link_capacity`.
- **Apply Phase:** Once all valid moves are decided, drones physically update their locations, and the output is generated.
- **Deadlock Detection:** If no drones can move and not all are delivered, the simulation raises a `RuntimeError` to prevent infinite loops.

## Visual Representation

The program provides visual feedback using ANSI escape codes.
When a map defines a color in the metadata (e.g., `[color=red]`), the visualizer maps it to the corresponding terminal color. The output highlights destination hubs in their designated colors, making it easier for the user to visually track the network and the flow of drones.

## Example Input and Expected Output

### Example Input (`map.txt`):

    nb_drones: 2
    start_hub: start 0 0 [color=green]
    hub: restricted 1 0 [zone=restricted color=red]
    end_hub: goal 2 0 [color=green]
    connection: start-restricted
    connection: restricted-goal

### Expected Output:

    D1-start-restricted
    D1-restricted D2-start-restricted
    D1-goal D2-restricted
    D2-goal

*(Notice how D1 spends a turn on the connection, and D2 starts crossing it on the exact same turn D1 arrives at the restricted zone.)*

## Resources

- [Dijkstra's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python `typing` Documentation](https://docs.python.org/3/library/typing.html)
- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- [ANSI Escape Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)

## AI Usage Disclosure

In accordance with the 42 AI guidelines, AI was used as a learning and debugging tutor rather than a code generator.
- **Tasks:** AI was used to explain complex logic (e.g., the "revolving door" simultaneous movement paradox), review Python typing errors (`mypy` union types), and help design the step-by-step architecture of the simulation loop.
- **Parts of the project:** AI assisted in conceptualizing the Dijkstra implementation and the state-management of the simulation. All code was written, debugged, and fully understood by the author to ensure defense readiness during peer review.
