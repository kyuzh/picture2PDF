import sys
import numpy as np
import pyautogui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt
from pynput import mouse


class ColorPickerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Picker")
        self.setGeometry(100, 100, 400, 200)

        # Définir la fenêtre pour qu'elle reste toujours au-dessus
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Label pour afficher la couleur et les coordonnées
        self.color_label = QLabel("Cliquez n'importe où sur l'écran pour obtenir la couleur du pixel", self)
        self.color_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.color_label)

        # Définir la politique de focus
        self.setFocusPolicy(Qt.StrongFocus)

    def update_color(self, x, y):
        # Capturer la couleur du pixel à ces coordonnées
        pixel_color = self.get_pixel_color(x, y)

        # Mettre à jour le label avec la couleur et les coordonnées
        self.color_label.setText(f"Position: ({x}, {y})\nCouleur: {pixel_color}")
        self.color_label.setStyleSheet(f"background-color: rgb{pixel_color};")

    def get_pixel_color(self, x, y):
        # Capturer une image de l'écran
        screenshot = pyautogui.screenshot()

        # Convertir l'image en tableau numpy
        screenshot_np = np.array(screenshot)

        # Vérifier si les coordonnées sont dans les limites de l'image
        if y < screenshot_np.shape[0] and x < screenshot_np.shape[1]:
            # Obtenir la couleur du pixel
            color = screenshot_np[y, x]
            # Retourner la couleur au format (R, G, B)
            return tuple(color)
        else:
            return (0, 0, 0)  # Retourne noir si hors des limites


class MouseListener:
    def __init__(self, app):
        self.app = app
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.app.update_color(x, y)  # Met à jour la couleur dans l'application


app = QApplication(sys.argv)

color_picker = ColorPickerApp()
color_picker.show()

mouse_listener = MouseListener(color_picker)

# Exécuter l'application
sys.exit(app.exec_())
