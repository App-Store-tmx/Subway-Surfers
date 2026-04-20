# app.py
import customtkinter as ctk
import tkinter as tk
import random
VERSION = "1.0.0"

# Enforce Termux environment aesthetic
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SubwayRunner(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Termux Runner")
        self.geometry("400x600")
        self.resizable(False, False)

        # Game State
        self.lanes = [50, 150, 250] # Center coordinates for the 3 lanes
        self.current_lane = 1
        self.score = 0
        self.speed = 10
        self.is_game_over = False
        self.obstacles = []

        # UI Overlay
        self.score_label = ctk.CTkLabel(self, text="Score: 0", font=("Arial", 24, "bold"))
        self.score_label.pack(pady=10)

        # Game Canvas
        self.canvas = tk.Canvas(self, width=300, height=500, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Draw Lanes (Visual flair)
        self.canvas.create_line(100, 0, 100, 500, fill="#333333", dash=(10, 10))
        self.canvas.create_line(200, 0, 200, 500, fill="#333333", dash=(10, 10))

        # Player (Blue Block)
        self.player = self.canvas.create_rectangle(
            self.lanes[self.current_lane] + 10, 430,
            self.lanes[self.current_lane] + 40, 480,
            fill="#1f538d", outline="#14375e", width=2
        )

        # Controls
        self.bind("<Left>", self.move_left)
        self.bind("<Right>", self.move_right)

        # Start Loop
        self.game_loop()

    def move_left(self, event):
        if self.current_lane > 0 and not self.is_game_over:
            self.current_lane -= 1
            self.update_player_position()

    def move_right(self, event):
        if self.current_lane < 2 and not self.is_game_over:
            self.current_lane += 1
            self.update_player_position()

    def update_player_position(self):
        x = self.lanes[self.current_lane] + 10
        self.canvas.coords(self.player, x, 430, x + 30, 480)

    def spawn_obstacle(self):
        lane = random.choice(self.lanes)
        # Red Block (Train/Obstacle)
        obs = self.canvas.create_rectangle(lane + 10, -50, lane + 40, 0, fill="#c93434", outline="#8a2323", width=2)
        self.obstacles.append(obs)

    def game_loop(self):
        if self.is_game_over:
            return

        self.score += 1
        self.score_label.configure(text=f"Score: {self.score}")

        # Spawn logic (Spawn rate increases slightly with speed)
        if random.randint(1, max(5, 20 - (self.speed // 2))) == 1:
            self.spawn_obstacle()

        new_obstacles = []
        for obs in self.obstacles:
            self.canvas.move(obs, 0, self.speed)
            coords = self.canvas.coords(obs)

            # Collision Detection (AABB)
            p_coords = self.canvas.coords(self.player)
            if (coords[2] > p_coords[0] and coords[0] < p_coords[2] and
                coords[3] > p_coords[1] and coords[1] < p_coords[3]):
                self.game_over()
                return

            # Cleanup off-screen obstacles
            if coords[1] > 500:
                self.canvas.delete(obs)
            else:
                new_obstacles.append(obs)

        self.obstacles = new_obstacles

        # Speed scaling
        if self.score % 300 == 0:
            self.speed += 1

        self.after(30, self.game_loop)

    def game_over(self):
        self.is_game_over = True
        self.canvas.create_rectangle(50, 200, 250, 300, fill="#2b2b2b", outline="#c93434", width=3)
        self.canvas.create_text(150, 250, text="GAME OVER", fill="white", font=("Arial", 24, "bold"))

if __name__ == "__main__":
    app = SubwayRunner()
    app.mainloop()