import random
import time
import tkinter as tk
from tkinter import messagebox

class GameOfLife:
    def __init__(self, root):
        self.root = root
        self.root.title("Game of Life")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        self.rows = 50
        self.cols = 100
        self.left_margin = 0
        self.cell_color = 'lime'
        self.auto_restart = False
        self.auto_color = False
        self.rainbow_fade = False
        self.random_numbers = False
        self.paused = False
        self.buttons_visible = True
        self.background_visible = True
        self.last_restart_time = time.time()
        self.restart_count = 0
        self.cell_positions = {}
        self.rainbow_hue = 0
        self.main_frame = tk.Frame(root, bg='black', padx=0, pady=0)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.button_frame = tk.Frame(self.main_frame, bg='black', padx=0, pady=0)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        self.counter_label = tk.Label(self.button_frame, text="Restarts: 0",
                                    font=('Arial', 12), bg='black', fg='white')
        self.counter_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.auto_restart_button = tk.Button(self.button_frame, text="Auto Restart: OFF", 
                                           command=self.toggle_auto_restart,
                                           font=('Arial', 12), bg='purple', fg='white',
                                           relief='flat')
        self.auto_restart_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.color_button = tk.Button(self.button_frame, text="Random Color: OFF", 
                                    command=self.toggle_auto_color,
                                    font=('Arial', 12), bg='blue', fg='white',
                                    relief='flat')
        self.color_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.rainbow_button = tk.Button(self.button_frame, text="Rainbow Fade: OFF", 
                                      command=self.toggle_rainbow_fade,
                                      font=('Arial', 12), bg='purple', fg='white',
                                      relief='flat')
        self.rainbow_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.background_button = tk.Button(self.button_frame, text="Background: ON", 
                                         command=self.toggle_background,
                                         font=('Arial', 12), bg='gray', fg='white',
                                         relief='flat')
        self.background_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.numbers_button = tk.Button(self.button_frame, text="Random Numbers: OFF", 
                                      command=self.toggle_random_numbers,
                                      font=('Arial', 12), bg='cyan', fg='black',
                                      relief='flat')
        self.numbers_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.pause_button = tk.Button(self.button_frame, text="Pause: OFF", 
                                    command=self.toggle_pause,
                                    font=('Arial', 12), bg='yellow', fg='black',
                                    relief='flat')
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.quit,
                                   font=('Arial', 12), bg='red', fg='white',
                                   relief='flat')
        self.quit_button.pack(side=tk.RIGHT, padx=10, pady=10)
        self.canvas = tk.Canvas(self.main_frame, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.grid = self.create_grid()
        self.prev_grid = None
        self.root.bind('<Return>', self.restart)
        self.root.bind('<Escape>', self.quit)
        self.root.bind('h', self.toggle_buttons)
        self.root.bind('H', self.toggle_buttons)
        self.update()
    
    def create_grid(self):
        return [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
    
    def count_neighbors(self, grid, row, col):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    count += grid[new_row][new_col]
        return count
    
    def update_grid(self):
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.count_neighbors(self.grid, i, j)
                if self.grid[i][j] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[i][j] = 0
                    else:
                        new_grid[i][j] = 1
                else:
                    if neighbors == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
        return new_grid
    
    def draw_grid(self):
        self.canvas.delete('all')
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        cell_width = (canvas_width - self.left_margin) / self.cols
        cell_height = canvas_height / self.rows
        font_size = min(int(cell_width * 0.8), int(cell_height * 0.8))
        if font_size < 1:
            font_size = 1
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:
                    x = j * cell_width + cell_width / 2 + self.left_margin
                    y = i * cell_height + cell_height / 2
                    if self.rainbow_fade:
                        hue = (self.rainbow_hue + (i + j) * 0.01) % 1.0
                        r, g, b = self.hsv_to_rgb(hue, 1.0, 1.0)
                        color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
                    else:
                        color = self.cell_color
                    cell_text = str(random.randint(0, 9)) if self.random_numbers else '0'
                    self.canvas.create_text(x, y, text=cell_text, fill=color, 
                                          font=('Courier', font_size))
        if self.rainbow_fade:
            self.rainbow_hue = (self.rainbow_hue + 0.01) % 1.0
    
    def update(self):
        if not self.paused:
            self.prev_grid = [row[:] for row in self.grid]
            self.grid = self.update_grid()
            self.draw_grid()
            current_time = time.time()
            if self.auto_restart and (self.check_game_ended() or current_time - self.last_restart_time >= 60):
                self.restart()
                self.last_restart_time = current_time
        self.root.after(50, self.update)
    
    def restart(self, event=None):
        self.grid = self.create_grid()
        self.last_restart_time = time.time()
        self.restart_count += 1
        self.counter_label.config(text=f"Restarts: {self.restart_count}")
        if self.auto_color:
            self.change_color()
    
    def quit(self, event=None):
        self.root.quit()
    
    def toggle_auto_restart(self):
        self.auto_restart = not self.auto_restart
        self.auto_restart_button.config(
            text="Auto Restart: ON" if self.auto_restart else "Auto Restart: OFF",
            bg='green' if self.auto_restart else 'purple'
        )
        if self.auto_restart:
            self.last_restart_time = time.time()
    
    def toggle_auto_color(self):
        self.auto_color = not self.auto_color
        self.color_button.config(
            text="Random Color: ON" if self.auto_color else "Random Color: OFF",
            bg='green' if self.auto_color else 'blue'
        )
        if self.auto_color:
            self.change_color()
    
    def toggle_rainbow_fade(self):
        self.rainbow_fade = not self.rainbow_fade
        self.rainbow_button.config(
            text="Rainbow Fade: ON" if self.rainbow_fade else "Rainbow Fade: OFF",
            bg='green' if self.rainbow_fade else 'purple'
        )
    
    def toggle_background(self):
        self.background_visible = not self.background_visible
        if self.background_visible:
            self.root.attributes('-alpha', 1.0)
        else:
            self.root.attributes('-alpha', 0.5)
        self.background_button.config(
            text="Background: ON" if self.background_visible else "Background: OFF",
            bg='green' if self.background_visible else 'gray'
        )
    
    def toggle_random_numbers(self):
        self.random_numbers = not self.random_numbers
        self.numbers_button.config(
            text="Random Numbers: ON" if self.random_numbers else "Random Numbers: OFF",
            bg='green' if self.random_numbers else 'cyan'
        )
    
    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(
            text="Pause: ON" if self.paused else "Pause: OFF",
            bg='green' if self.paused else 'yellow'
        )
    
    def toggle_buttons(self, event=None):
        self.buttons_visible = not self.buttons_visible
        if self.buttons_visible:
            self.button_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        else:
            self.button_frame.pack_forget()
    
    def change_color(self):
        colors = ['red', 'orange', 'yellow', 'lime', 'cyan', 'blue', 'magenta', 'white']
        self.cell_color = random.choice(colors)
        self.draw_grid()
    
    def hsv_to_rgb(self, h, s, v):
        if s == 0.0:
            return v, v, v
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q
    
    def check_game_ended(self):
        if self.prev_grid is None:
            return False
        return all(
            self.grid[i][j] == self.prev_grid[i][j]
            for i in range(self.rows)
            for j in range(self.cols)
        )

def main():
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()

if __name__ == "__main__":
    main() 