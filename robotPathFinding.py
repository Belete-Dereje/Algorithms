from collections import deque

def bfs_grid(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = set([start])

    directions = [(0,1),(1,0),(0,-1),(-1,0)]

    while queue:
        (x,y), path = queue.popleft()

        if (x,y) == goal:
            return path

        for dx, dy in directions:
            nx, ny = x+dx, y+dy

            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                if (nx,ny) not in visited:
                    visited.add((nx,ny))
                    queue.append(((nx,ny), path + [(nx,ny)]))

    return None

grid = [
    [0,0,0,0,0],
    [0,1,1,0,0],
    [0,0,0,1,0],
    [1,0,0,0,0],
    [0,0,0,0,0]
]

print(bfs_grid(grid, (0,0), (4,4)))