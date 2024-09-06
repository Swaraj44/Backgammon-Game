import tkinter as tk
from tkinter import ttk

import BGMN as BG

# Function to open a new window with the chosen mode
def open_mode_window(mode):
    
    if mode=="Normal":
        mode='n'
    else:
        mode='h'
    
    root.destroy()
    BG.mainMenu(mode)
    
    

# Main window
root = tk.Tk()
root.title("Backgammon")
root.geometry("900x300")
root.resizable(width=False, height=False)
root.configure(bg='black')  # Set background color to black

# Main window layout
title_label = ttk.Label(root, text="Backgammon", font=("Arial", 16), foreground='red', background='black')
title_label.pack(pady=10)

mode_label = ttk.Label(root, text="Choose your Opponent:", font=("Arial", 12), foreground='red', background='black')
mode_label.pack(pady=5)

# Button styling
style = ttk.Style()
style.configure('Red.TButton', foreground='red', background='black', font=("Arial", 10))

# Centering frame for buttons
buttons_frame = tk.Frame(root, bg='black')
buttons_frame.pack(pady=20)  

# Buttons
normal_button = ttk.Button(buttons_frame, text="JARVIS AI", command=lambda: open_mode_window("Normal"), style='Red.TButton')
normal_button.pack(pady=10)  

hard_button = ttk.Button(buttons_frame, text="EDITH AI", command=lambda: open_mode_window("Hard"), style='Red.TButton')
hard_button.pack(pady=10)

# Center the buttons frame in the main window
buttons_frame.pack(anchor='center')

# Start the GUI event loop
root.mainloop()
