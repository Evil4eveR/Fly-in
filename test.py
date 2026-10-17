
maze = [
    ["S", ".", "#"],
    [".", ".", "."],
    [".", "#", "#"],
    [".", ".", "G"]
]

size_i = len(maze)
size_j = len(maze[0])

visited = {(0, 0)}
to_visit = [(0, 0)]

found = False
directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

while to_visit:
    curr = to_visit.pop()

    i,j = curr
    if maze[i][j] == 'G':
        found = True
        break
    for di, dj in directions:
        ni, nj = curr[0] + di, curr[1] + dj
        if ni >= 0 and nj >= 0 and nj < size_j and ni < size_i and maze[ni][nj] != "#":
            if (ni, nj) not in visited:
                visited.add((ni, nj))
                to_visit.append((ni, nj))

print(found)
