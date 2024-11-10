# utils.py
import pyautogui
import keyboard
import threading

def get_mouse_position_on_keypress():
    print("Press Ctrl + Space to get the mouse position...")
    keyboard.wait('ctrl + space')  # Wait for the key combination
    x, y = pyautogui.position()  # Get the current mouse position
    print(f"Mouse position: ({x}, {y})")
    return x, y

def start_mouse_listener():
    mouse_listener_thread = threading.Thread(target=get_mouse_position_on_keypress)
    mouse_listener_thread.daemon = True  # This will allow the program to exit even if this thread is running
    mouse_listener_thread.start()
