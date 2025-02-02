import cv2
import numpy as np
from ultralytics import YOLO
import serial
import time
from PIL import ImageGrab

# Charger le modèle YOLOv5s pré-entraîné ou personnalisé (best.pt)
model = YOLO('best.pt')  # Utilise un modèle plus léger (par exemple, YOLOv5s)

# Configurer la connexion série avec l'Arduino
arduino = serial.Serial('COM10', 9600)  # Remplacez 'COMx' par le bon port COM
time.sleep(2)  # Attendre la connexion série stable

# Fonction pour envoyer des commandes à l'Arduino pour déplacer la souris
def send_command_to_arduino(command):
    arduino.write(command.encode())  # Envoi de la commande à l'Arduino

# Fonction pour déplacer la souris en fonction des coordonnées
def move_mouse(center_x, center_y, screen_width, screen_height):
    # Calcul des décalages relatifs par rapport au centre de l'écran
    x_offset = int((center_x - screen_width // 2) / (screen_width // 2) * 100)  # De -100 à 100
    y_offset = int((center_y - screen_height // 2) / (screen_height // 2) * 100)  # De -100 à 100

    # Envoi des commandes à l'Arduino en fonction des décalages
    if x_offset < -10:
        send_command_to_arduino('L')  # Déplacer à gauche
    elif x_offset > 10:
        send_command_to_arduino('R')  # Déplacer à droite

    if y_offset < -10:
        send_command_to_arduino('U')  # Déplacer vers le haut
    elif y_offset > 10:
        send_command_to_arduino('D')  # Déplacer vers le bas

# Capture de l'écran en temps réel (ImageGrab)
def capture_screen():
    # Prend une capture d'écran de la zone spécifiée (ici l'écran entier)
    screen = np.array(ImageGrab.grab())
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)  # Convertir l'image en BGR pour OpenCV
    return screen

# Boucle principale
while True:
    # Capturer l'écran en temps réel et réduire la résolution pour améliorer la vitesse
    frame = capture_screen()
    frame = cv2.resize(frame, (640, 640))  # Réduire la taille à 640x640 pour accélérer le traitement

    # Appliquer YOLOv5 sur l'image capturée
    results = model(frame)  # Appliquer YOLOv5
    boxes = results[0].boxes  # Récupérer les boîtes de détection

    if len(boxes) > 0:
        # Si des objets sont détectés, récupérer le centre du premier objet détecté
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Coordonnées de la boîte de détection
            center_x = int((x1 + x2) / 2)  # Calculer le centre de l'objet (axe X)
            center_y = int((y1 + y2) / 2)  # Calculer le centre de l'objet (axe Y)

            # Dimensions de l'écran capturé
            screen_width = frame.shape[1]
            screen_height = frame.shape[0]

            # Déplacer la souris en fonction du centre de l'objet détecté
            move_mouse(center_x, center_y, screen_width, screen_height)

    # Afficher l'image avec les objets détectés pour vérifier visuellement
    cv2.imshow('Detection', frame)

    # Quitter si 'q' est pressé
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
