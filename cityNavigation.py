import tkinter as tk
from tkinter import ttk, messagebox
import heapq

# ---------------- GRAPH ----------------
graph = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
    "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
    "Craiova": [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
    "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
    "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
    "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
    "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
    "Giurgiu": [("Bucharest", 90)],
    "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
    "Eforie": [("Hirsova", 86)],
    "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
    "Iasi": [("Vaslui", 92), ("Neamt", 87)],
    "Neamt": [("Iasi", 87)]
}

heuristic = {
    "Arad": 366, "Zerind": 374, "Oradea": 380, "Sibiu": 253,
    "Timisoara": 329, "Lugoj": 244, "Mehadia": 241, "Drobeta": 242,
    "Craiova": 160, "Rimnicu Vilcea": 193, "Fagaras": 176,
    "Pitesti": 100, "Bucharest": 0, "Giurgiu": 77,
    "Urziceni": 80, "Hirsova": 151, "Eforie": 161,
    "Vaslui": 199, "Iasi": 226, "Neamt": 234
}

# ---------------- ALGORITHMS ----------------

def ucs(start, goal):
    pq = [(0, start, [])]
    visited = set()

    while pq:
        cost, city, path = heapq.heappop(pq)

        if city in visited:
            continue
        visited.add(city)

        path = path + [city]

        if city == goal:
            return path, cost

        for neighbor, dist in graph[city]:
            heapq.heappush(pq, (cost + dist, neighbor, path))

def astar(start, goal):
    pq = [(heuristic[start], 0, start, [])]
    visited = set()

    while pq:
        f, g, city, path = heapq.heappop(pq)

        if city in visited:
            continue
        visited.add(city)

        path = path + [city]

        if city == goal:
            return path, g

        for neighbor, dist in graph[city]:
            new_g = g + dist
            new_f = new_g + heuristic[neighbor]
            heapq.heappush(pq, (new_f, new_g, neighbor, path))

# ---------------- GUI ----------------

class RomaniaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Romania Map AI Search")

        self.create_ui()
        self.draw_map()

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()

        self.start = tk.StringVar(value="Arad")
        self.goal = tk.StringVar(value="Bucharest")
        self.algorithm = tk.StringVar(value="A*")

        cities = list(graph.keys())

        ttk.Label(frame, text="Start").grid(row=0, column=0)
        ttk.Combobox(frame, values=cities, textvariable=self.start).grid(row=0, column=1)

        ttk.Label(frame, text="Goal").grid(row=0, column=2)
        ttk.Combobox(frame, values=cities, textvariable=self.goal).grid(row=0, column=3)

        ttk.Label(frame, text="Algorithm").grid(row=0, column=4)
        ttk.Combobox(frame, values=["UCS", "A*"], textvariable=self.algorithm).grid(row=0, column=5)

        tk.Button(frame, text="Run", command=self.run).grid(row=0, column=6)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack()

        self.canvas = tk.Canvas(self.root, width=800, height=500, bg="white")
        self.canvas.pack()

    # -------- DRAW MAP (simple layout) --------
    def draw_map(self):
        self.positions = {
            "Arad": (100, 250), "Zerind": (100, 150), "Oradea": (150, 80),
            "Sibiu": (250, 200), "Timisoara": (100, 350), "Lugoj": (180, 380),
            "Mehadia": (180, 430), "Drobeta": (180, 480), "Craiova": (300, 480),
            "Rimnicu Vilcea": (300, 300), "Fagaras": (400, 200),
            "Pitesti": (400, 350), "Bucharest": (550, 350),
            "Giurgiu": (550, 450), "Urziceni": (650, 300),
            "Hirsova": (750, 300), "Eforie": (800, 380),
            "Vaslui": (650, 200), "Iasi": (650, 120), "Neamt": (650, 60)
        }

        # draw edges
        for city in graph:
            for neighbor, _ in graph[city]:
                x1,y1 = self.positions[city]
                x2,y2 = self.positions[neighbor]
                self.canvas.create_line(x1,y1,x2,y2)

        # draw nodes
        for city, (x,y) in self.positions.items():
            self.canvas.create_oval(x-15,y-15,x+15,y+15,fill="lightblue")
            self.canvas.create_text(x,y,text=city,font=("Arial",8))

    def run(self):
        start = self.start.get()
        goal = self.goal.get()
        algo = self.algorithm.get()

        if algo == "UCS":
            path, cost = ucs(start, goal)
        else:
            path, cost = astar(start, goal)

        self.result_label.config(
            text=f"Path: {' → '.join(path)} | Cost: {cost}"
        )

        self.highlight_path(path)

    def highlight_path(self, path):
        self.draw_map()

        for i in range(len(path)-1):
            x1,y1 = self.positions[path[i]]
            x2,y2 = self.positions[path[i+1]]
            self.canvas.create_line(x1,y1,x2,y2,fill="red",width=3)

# RUN
root = tk.Tk()
app = RomaniaGUI(root)
root.mainloop()