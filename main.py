import tkinter as tk
import subprocess

# Function to update the label with the button that was clicked and run another script
def button_clicked(button_name, script_name):
    label.config(text=f"{button_name} button was clicked")
    root.destroy()
    subprocess.run(["python", script_name])

# Create the main window
root = tk.Tk()
root.title("AI Project")

# Set the size of the window
root.geometry("400x300")

# Create a label to display which button was clicked
label = tk.Label(root, text="Choose The Algorithm", font=("Helvetica", 14,"bold"))
label.pack(pady=20)

# Customizing button styles
button_style = {
    "font": ("Helvetica", 14),
    "bg": "lightblue",
    "fg": "darkblue",
    "activebackground": "blue",
    "activeforeground": "white",
    "width": 12,
    "height": 2,
    "relief": tk.RAISED,
    "bd": 5
}

# Create the "A star" button and specify the script to run
astar_button = tk.Button(root, text="A star", command=lambda: button_clicked("A star", "A_star.py"), **button_style)
astar_button.pack(side=tk.LEFT, padx=20, pady=10)

# Create the "Genetic" button and specify the script to run
genetic_button = tk.Button(root, text="Genetic", command=lambda: button_clicked("Genetic", "Genetic.py"), **button_style)
genetic_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Start the main event loop
root.mainloop()
