import tkinter as tk
import random
import heapq
from tkinter import messagebox

GOAL = (1,2,3,4,5,6,7,8,0)

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver (A*)")

        self.state = list(GOAL)
        self.buttons = []

        self.create_ui()
        self.draw()

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(9):
            btn = tk.Button(frame, text="", width=6, height=3,
                            font=("Arial", 18),
                            command=lambda i=i: self.move(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

        control = tk.Frame(self.root)
        control.pack(pady=10)

        tk.Button(control, text="Shuffle", command=self.shuffle).grid(row=0, column=0)
        tk.Button(control, text="Solve (A*)", command=self.solve).grid(row=0, column=1)
        tk.Button(control, text="Reset", command=self.reset).grid(row=0, column=2)

        self.info = tk.Label(self.root, text="")
        self.info.pack()

    def draw(self):
        for i in range(9):
            value = self.state[i]
            text = "" if value == 0 else str(value)
            self.buttons[i].config(text=text, bg="white")

    def move(self, i):
        zero = self.state.index(0)
        if i in self.get_neighbors(zero):
            self.state[zero], self.state[i] = self.state[i], self.state[zero]
            self.draw()

    def get_neighbors(self, index):
        x, y = divmod(index, 3)
        moves = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                moves.append(nx*3+ny)
        return moves

    def shuffle(self):
        self.state = list(GOAL)
        for _ in range(50):
            zero = self.state.index(0)
            neighbors = self.get_neighbors(zero)
            swap = random.choice(neighbors)
            self.state[zero], self.state[swap] = self.state[swap], self.state[zero]
        self.draw()
        self.info.config(text="Shuffled!")

    def reset(self):
        self.state = list(GOAL)
        self.draw()
        self.info.config(text="Reset")

    # ---------- A* SEARCH ----------

    def heuristic(self, state):
        return sum(1 for i in range(9) if state[i] != 0 and state[i] != GOAL[i])

    def astar(self, start):
        pq = [(self.heuristic(start), 0, tuple(start), [])]
        visited = set()

        while pq:
            f, g, state, path = heapq.heappop(pq)

            if state in visited:
                continue
            visited.add(state)

            path = path + [state]

            if state == GOAL:
                return path

            zero = state.index(0)
            for n in self.get_neighbors(zero):
                new_state = list(state)
                new_state[zero], new_state[n] = new_state[n], new_state[zero]
                heapq.heappush(pq, (
                    g + 1 + self.heuristic(new_state),
                    g + 1,
                    tuple(new_state),
                    path
                ))

        return None

    def solve(self):
        self.info.config(text="Solving...")
        self.root.update()

        solution = self.astar(self.state)

        if not solution:
            messagebox.showinfo("Result", "No solution found")
            return

        self.info.config(text=f"Steps: {len(solution)-1}")
        self.animate(solution)

    def animate(self, solution):
        def step(i):
            if i >= len(solution):
                return
            self.state = list(solution[i])
            self.draw()
            self.root.after(300, lambda: step(i+1))

        step(0)

# RUN
root = tk.Tk()
app = PuzzleGUI(root)
root.mainloop()