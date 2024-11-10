import pyautogui
from pywinauto import Application, findwindows
import time

import picture
from setting import Path_projet, MEADIA_Path
import utile

# Use the imported variables
print(f"Current project path: {Path_projet}")
print(f"Media path: {MEADIA_Path}")
time.sleep(8)
# List all open windows
windows = findwindows.find_elements()
for window in windows:
    print(f"Title: {window.name}, Class: {window.class_name}, Handle: {window.handle}")

name_window = "readerlb.cyberlibris.com/api/js/book/"
# Attempt to connect to a specific Microsoft Edge window
app = Application(backend="win32").connect(
    title_re=name_window)
main_window = app.window(title_re=name_window)

main_window.set_focus()
# Get the window's rectangle
rect = main_window.rectangle()  # This will get the position and size of the window
# Calculate the center of the window
center_x = rect.left + 5
center_y = rect.top + (rect.height() // 2)
# Optional: Give a moment to see the mouse move

for i in range(0,246):

    time.sleep(1)
    # Move the mouse to the center of the main window
    pyautogui.moveTo(center_x, center_y)
    contour = picture.capture_and_detect_contours(target_area=1000000, tolerance=618000)
    print(contour)
    picture.capture_and_save_area(contour, fr"C:\Users\manji\Desktop\livre\data9\output_path{i}.png")
    # Scroll down by 1300 units

    pyautogui.scroll(-contour[3])  # Negative value for scrolling down
