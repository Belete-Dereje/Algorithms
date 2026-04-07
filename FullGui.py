import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import heapq

ROWS, COLS = 10, 10
CELL_SIZE = 40

class AIVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Search Visualizer")

        self.grid = [[0]*COLS for _ in range(ROWS)]
        self.start = None
        self.goal = None
        self.mode = "obstacle"

        self.algorithm = tk.StringVar(value="BFS")

        self.create_ui()
        self.draw_grid()

    def create_ui(self):
        top = tk.Frame(self.root)
        top.pack()

        ttk.Label(top, text="Algorithm:").grid(row=0, column=0)

        algo_menu = ttk.Combobox(top, textvariable=self.algorithm, values=[
            "BFS", "DFS", "A*", "UCS"
        ])
        algo_menu.grid(row=0, column=1)

        tk.Button(top, text="Run", command=self.run).grid(row=0, column=2)
        tk.Button(top, text="Clear", command=self.clear).grid(row=0, column=3)

        tk.Button(top, text="Start", command=lambda: self.set_mode("start")).grid(row=1, column=0)
        tk.Button(top, text="Goal", command=lambda: self.set_mode("goal")).grid(row=1, column=1)
        tk.Button(top, text="Obstacle", command=lambda: self.set_mode("obstacle")).grid(row=1, column=2)

        self.canvas = tk.Canvas(self.root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(ROWS):
            for j in range(COLS):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1+CELL_SIZE, y1+CELL_SIZE

                color = "white"
                if self.grid[i][j] == 1:
                    color = "black"
                if (i,j) == self.start:
                    color = "green"
                if (i,j) == self.goal:
                    color = "red"

                self.canvas.create_rectangle(x1,y1,x2,y2,fill=color, outline="gray")

    def on_click(self, event):
        r = event.y // CELL_SIZE
        c = event.x // CELL_SIZE

        if self.mode == "start":
            self.start = (r,c)
        elif self.mode == "goal":
            self.goal = (r,c)
        elif self.mode == "obstacle":
            self.grid[r][c] = 1

        self.draw_grid()

    def set_mode(self, mode):
        self.mode = mode

    def clear(self):
        self.grid = [[0]*COLS for _ in range(ROWS)]
        self.start = None
        self.goal = None
        self.draw_grid()

    def neighbors(self, node):
        x,y = node
        dirs = [(0,1),(1,0),(0,-1),(-1,0)]
        res = []
        for dx,dy in dirs:
            nx,ny = x+dx, y+dy
            if 0<=nx<ROWS and 0<=ny<COLS and self.grid[nx][ny]==0:
                res.append((nx,ny))
        return res

    # ---------------- ALGORITHMS ----------------

    def bfs(self):
        q = deque([(self.start,[self.start])])
        visited = set([self.start])

        while q:
            node,path = q.popleft()
            if node == self.goal:
                return path

            for n in self.neighbors(node):
                if n not in visited:
                    visited.add(n)
                    q.append((n,path+[n]))

    def dfs(self):
        stack = [(self.start,[self.start])]
        visited = set()

        while stack:
            node,path = stack.pop()
            if node == self.goal:
                return path

            if node not in visited:
                visited.add(node)
                for n in self.neighbors(node):
                    stack.append((n,path+[n]))

    def ucs(self):
        pq = [(0,self.start,[self.start])]
        visited = set()

        while pq:
            cost,node,path = heapq.heappop(pq)

            if node in visited:
                continue
            visited.add(node)

            if node == self.goal:
                return path

            for n in self.neighbors(node):
                heapq.heappush(pq,(cost+1,n,path+[n]))

    def heuristic(self,a,b):
        return abs(a[0]-b[0])+abs(a[1]-b[1])

    def astar(self):
        pq = [(0,self.start,[self.start])]
        visited = set()

        while pq:
            cost,node,path = heapq.heappop(pq)

            if node in visited:
                continue
            visited.add(node)

            if node == self.goal:
                return path

            for n in self.neighbors(node):
                new_cost = len(path) + self.heuristic(n,self.goal)
                heapq.heappush(pq,(new_cost,n,path+[n]))

    # ---------------- RUN ----------------

    def run(self):
        if not self.start or not self.goal:
            messagebox.showerror("Error","Set start and goal")
            return

        algo = self.algorithm.get()

        if algo == "BFS":
            path = self.bfs()
        elif algo == "DFS":
            path = self.dfs()
        elif algo == "UCS":
            path = self.ucs()
        elif algo == "A*":
            path = self.astar()

        if path:
            self.draw_path(path)
        else:
            messagebox.showinfo("Result","No path found")

    def draw_path(self,path):
        for (i,j) in path:
            if (i,j)!=self.start and (i,j)!=self.goal:
                x1,y1 = j*CELL_SIZE, i*CELL_SIZE
                x2,y2 = x1+CELL_SIZE, y1+CELL_SIZE
                self.canvas.create_rectangle(x1,y1,x2,y2,fill="blue")

# RUN APP
root = tk.Tk()
app = AIVisualizer(root)
root.mainloop()