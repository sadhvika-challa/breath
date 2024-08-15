import tkinter as tk
from PIL import Image, ImageTk

class BreathApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Breath Control")
        self.geometry("450x200")

        # Load the background image
        self.bg_image = Image.open("background.png")
        self.bg_image = self.bg_image.resize((450, 200), Image.Resampling.LANCZOS)  # Resize to fit canvas
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas with a light gray background
        self.canvas = tk.Canvas(self, width=450, height=200, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Set the background image
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.radius = 10
        self.parabola_width = 317
        self.parabola_height = 125
        self.x_center = 70 + self.parabola_width // 2  # X-coordinate of the vertex (center)
        self.y_vertex = 42  # Y-coordinate of the vertex (top)

        # Draw the parabolic path with the requested stroke and color
        self.draw_parabolic_path()

        # Create the circle
        self.circle = self.canvas.create_oval(
            self.x_center - self.radius, 
            self.y_vertex - self.radius, 
            self.x_center + self.radius, 
            self.y_vertex + self.radius, 
            fill="white", outline=""
        )

        # Center the text relative to the parabola
        self.label = self.canvas.create_text(
            self.x_center, 
            self.y_vertex + self.parabola_height // 2, 
            text="", 
            font=("Lora Italic", 16, "italic"),
            fill="white"
        )

        # Create a transparent "Repeat" button directly on the canvas
        self.repeat_button = tk.Button(self.canvas, text="repeat", font=("Lora", 10), command=self.start_animation, bg="white", fg="black", bd=0, highlightthickness=0)
        self.canvas.create_window(195, 162, window=self.repeat_button, anchor="nw")

        # Initialize the time counter and animation state
        self.time = 0
        self.running = False

        # Start the animation when the app launches
        self.start_animation()

    def draw_parabolic_path(self):
        a = 4 * (self.parabola_height - self.y_vertex - self.radius) / (self.parabola_width - 2 * self.radius)**2
        path_coords = []

        for i in range(self.parabola_width):
            x = i + 70
            y = a * (x - self.x_center)**2 + self.y_vertex
            path_coords.append((x, y))

        for i in range(1, len(path_coords)):
            self.canvas.create_line(
                path_coords[i-1][0], path_coords[i-1][1], 
                path_coords[i][0], path_coords[i][1], 
                fill="white", width=2
            )

    def start_animation(self):
        if not self.running:
            self.time = 0  # Reset the time counter
            self.running = True
            self.animate()

    def animate(self):
        if not self.running:
            return
        
        self.time += 0.05
        x, y = self.calculate_position(self.time)

        self.canvas.coords(
            self.circle, 
            x - self.radius, 
            y - self.radius, 
            x + self.radius, 
            y + self.radius
        )

        phase = self.time % 19
        if phase < 4:
            self.canvas.itemconfig(self.label, text="inhale")
        elif phase < 11:
            self.canvas.itemconfig(self.label, text="hold")
        else:
            self.canvas.itemconfig(self.label, text="exhale")

        # Stop the animation if the ball reaches the bottom of the parabola
        if self.time >= 19:
            self.running = False
        else:
            self.after(50, self.animate)

    def calculate_position(self, time):
        total_time = 19
        phase = time % total_time

        a = 4 * (self.parabola_height - self.y_vertex - self.radius) / (self.parabola_width - 2 * self.radius)**2

        if phase < 4:
            t = phase / 4
            x = (self.radius + t * (self.parabola_width / 2 - 2 * self.radius)) + 70
            y = a * (x - self.x_center)**2 + self.y_vertex
        elif phase < 11:
            x = self.x_center
            y = self.y_vertex
        else:
            t = (phase - 11) / 8
            x = self.x_center + t * (self.parabola_width - self.x_center - self.radius)
            y = a * (x - self.x_center)**2 + self.y_vertex

        return x, y

if __name__ == "__main__":
    app = BreathApp()
    app.mainloop()
