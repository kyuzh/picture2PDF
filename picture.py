import pyautogui
from PIL import Image, ImageDraw
import numpy as np
import cv2
import time
from setting import Path_projet, MEADIA_Path
from pathlib import Path
import pyautogui
import keyboard

def capture_and_highlight_area(left, top, right, bottom):
    # Capture the screen
    screenshot = pyautogui.screenshot()

    # Draw a rectangle on the image
    draw = ImageDraw.Draw(screenshot)
    draw.rectangle([left, top, right, bottom], outline="red", width=5)  # Red highlight

    # Display the image
    screenshot.show()

# picture.capture_and_highlight_area2(coordinates)
def capture_and_highlight_area2(coordinates):
    # Parse the input string to extract coordinates
    coords = [int(num[1:]) for num in coordinates.split(', ')]

    # Unpack the coordinates
    left, top, right, bottom = coords

    # Capture the screen
    screenshot = pyautogui.screenshot()

    # Draw a rectangle on the image
    draw = ImageDraw.Draw(screenshot)
    draw.rectangle([left, top, right, bottom], outline="red", width=5)  # Red highlight

    # Display the image
    screenshot.show()


# picture.click_on_image(image_name)
def click_on_image(image_name):
    image_path = Path(MEADIA_Path) / image_name  # Use Path for better path handling

    # Give some time to prepare before capturing the screen
    time.sleep(2)

    # Capture the screen
    screenshot = pyautogui.screenshot()

    # Convert screenshot to a NumPy array
    screenshot_np = np.array(screenshot)

    # Convert from BGR to RGB
    screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)

    # Load the image to find
    target_image = cv2.imread(str(image_path))
    if target_image is None:
        print("The specified image could not be found.")
        return

    # Find the coordinates of the image in the screenshot
    result = cv2.matchTemplate(screenshot_rgb, target_image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Adjust this threshold as needed
    yloc, xloc = np.where(result >= threshold)

    # If a match is found, perform the click
    if len(xloc) > 0 and len(yloc) > 0:
        # Get the center of the first match
        x_center = xloc[0] + target_image.shape[1] // 2
        y_center = yloc[0] + target_image.shape[0] // 2

        # Simulate the click
        pyautogui.click(x=x_center, y=y_center)
        print(f"Click performed at coordinates: ({x_center}, {y_center})")
    else:
        print("No match found.")
# picture.capture_and_detect_contours()
def capture_and_detect_contours(target_area=1500, tolerance=20):
    # Capture d'écran
    screenshot = pyautogui.screenshot()
    contour_match = []

    # Conversion en tableau numpy au format BGR (utilisé par OpenCV)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Appliquer un flou pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Détection des contours avec Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Trouver les contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Parcourir les contours pour dessiner les rectangles
    for i, contour in enumerate(contours):
        # Calculer le rectangle englobant
        x, y, w, h = cv2.boundingRect(contour)
        # Calculer l'aire du contour
        area = (w)*(h)
        # Afficher les informations sur le contour et son rectangle englobant

        if abs(area - target_area) < tolerance:
            print(area - target_area)
            print(f"Contour - Rectangle: x={x}, y={y}, width={w}, height={h} - Aire: {area}")
            contour_match = [x, y, x + w, y + h]
            print(contour_match)
            return contour_match

    print(contour_match)
    return contour_match
def capture_and_detect_color_contours(target_color, tolerance=30):
    # Capture d'écran
    screenshot = pyautogui.screenshot()

    # Conversion en tableau numpy au format BGR (utilisé par OpenCV)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Convertir l'image en HSV pour la détection de couleurs
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Définir les limites de la couleur cible
    lower_color = np.array([max(0, target_color[0] - tolerance), 100, 100])  # Ajustez la saturation et la valeur selon vos besoins
    upper_color = np.array([min(180, target_color[0] + tolerance), 255, 255])  # 180 est la valeur max pour la teinte en HSV

    # Créer un masque pour détecter les zones de la couleur cible
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Trouver les contours dans le masque
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Parcourir les contours pour dessiner les rectangles
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Filtrer les petits contours
            x, y, w, h = cv2.boundingRect(contour)
            # Dessiner le rectangle sur l'image originale
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Afficher le résultat
    cv2.imshow("Color Matching Contours", frame)

    # Attendre qu'une touche soit pressée pour fermer la fenêtre
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#picture.capture_and_save_area(coords, output_path)
def capture_and_save_area(coords, output_path):
    # Extraire les coordonnées de la liste
    x1, y1, x2, y2 = coords

    # Définir la région à capturer
    region = (x1, y1, x2 - x1, y2 - y1)

    # Capturer la zone spécifiée
    screenshot = pyautogui.screenshot(region=region)

    # Convertir l'image en tableau numpy au format BGR (utilisé par OpenCV)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Optionnel : redimensionner l'image pour améliorer la qualité si nécessaire
    # Par exemple, doubler la taille de l'image avec interpolation de haute qualité
    # Note : Cela peut ne pas être nécessaire, en fonction de vos besoins
    # frame = cv2.resize(frame, (frame.shape[1] * 2, frame.shape[0] * 2), interpolation=cv2.INTER_CUBIC)

    # Sauvegarder l'image capturée au format PNG pour éviter la compression
    cv2.imwrite(output_path, frame, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    print(f"Image sauvegardée à : {output_path}")
