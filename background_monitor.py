import tkinter as tk
from tkinter import messagebox  # Import messagebox separately
import threading
import time
from pynput import keyboard, mouse

# Global flag to check if the unlock key was pressed
unlock_key_pressed = False

# Function to show the popup warning
def show_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    root.after(0, messagebox.showwarning, "Alert", "Unauthorized use detected!")  # ✅ Run in main loop
    root.mainloop()

# Function to listen for the unlock key (e.g., CTRL)
def key_listener():
    global unlock_key_pressed

    def on_press(key):
        global unlock_key_pressed
        if key == keyboard.Key.ctrl_l:  # Change this key if needed
            unlock_key_pressed = True

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Function to monitor activity
def activity_monitor():
    global unlock_key_pressed
    time.sleep(5)  # Give the user 5 seconds to enter the key

    # Start listening for activity
    def trigger_popup(*args):
        if not unlock_key_pressed:
            show_popup()

    with mouse.Listener(on_move=trigger_popup, on_click=trigger_popup), \
         keyboard.Listener(on_press=trigger_popup):
        while True:
            time.sleep(1)

# Run the key listener in a separate thread
threading.Thread(target=key_listener, daemon=True).start()
activity_monitor()

