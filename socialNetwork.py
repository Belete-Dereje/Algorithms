from collections import deque

def bfs_social(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        person, path = queue.popleft()

        if person == goal:
            return path

        for friend in graph[person]:
            if friend not in visited:
                visited.add(friend)
                queue.append((friend, path + [friend]))

    return None

social_graph = {
    "Alice": ["Bob", "Claire"],
    "Bob": ["Alice", "David"],
    "Claire": ["Alice", "Eve"],
    "David": ["Bob"],
    "Eve": ["Claire"]
}

print(bfs_social(social_graph, "Alice", "Eve"))