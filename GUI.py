import tkinter as tk
from tkinter import messagebox
from collections import deque
import heapq

ROWS, COLS = 10, 10
CELL_SIZE = 40

class PathfindingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Search Visualizer")

        self.grid = [[0]*COLS for _ in range(ROWS)]
        self.start = None
        self.goal = None

        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Set Start", command=self.set_start_mode).grid(row=0, column=0)
        tk.Button(btn_frame, text="Set Goal", command=self.set_goal_mode).grid(row=0, column=1)
        tk.Button(btn_frame, text="Add Obstacles", command=self.set_obstacle_mode).grid(row=0, column=2)
        tk.Button(btn_frame, text="Run BFS", command=self.run_bfs).grid(row=0, column=3)
        tk.Button(btn_frame, text="Run A*", command=self.run_astar).grid(row=0, column=4)
        tk.Button(btn_frame, text="Clear", command=self.clear).grid(row=0, column=5)

        self.mode = "obstacle"
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(ROWS):
            for j in range(COLS):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                color = "white"
                if self.grid[i][j] == 1:
                    color = "black"
                if self.start == (i,j):
                    color = "green"
                if self.goal == (i,j):
                    color = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def on_click(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if self.mode == "start":
            self.start = (row, col)
        elif self.mode == "goal":
            self.goal = (row, col)
        elif self.mode == "obstacle":
            self.grid[row][col] = 1

        self.draw_grid()

    def set_start_mode(self):
        self.mode = "start"

    def set_goal_mode(self):
        self.mode = "goal"

    def set_obstacle_mode(self):
        self.mode = "obstacle"

    def clear(self):
        self.grid = [[0]*COLS for _ in range(ROWS)]
        self.start = None
        self.goal = None
        self.draw_grid()

    def get_neighbors(self, node):
        x, y = node
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        result = []

        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < ROWS and 0 <= ny < COLS:
                if self.grid[nx][ny] == 0:
                    result.append((nx, ny))

        return result

    def run_bfs(self):
        if not self.start or not self.goal:
            messagebox.showerror("Error", "Set start and goal first!")
            return

        queue = deque([(self.start, [self.start])])
        visited = set([self.start])

        while queue:
            node, path = queue.popleft()

            if node == self.goal:
                self.draw_path(path)
                return

            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        messagebox.showinfo("Result", "No path found")

    def heuristic(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def run_astar(self):
        if not self.start or not self.goal:
            messagebox.showerror("Error", "Set start and goal first!")
            return

        pq = [(0, self.start, [self.start])]
        visited = set()

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node in visited:
                continue
            visited.add(node)

            if node == self.goal:
                self.draw_path(path)
                return

            for neighbor in self.get_neighbors(node):
                new_cost = len(path) + self.heuristic(neighbor, self.goal)
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

        messagebox.showinfo("Result", "No path found")

    def draw_path(self, path):
        for (i,j) in path:
            if (i,j) != self.start and (i,j) != self.goal:
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

root = tk.Tk()
app = PathfindingGUI(root)
root.mainloop()