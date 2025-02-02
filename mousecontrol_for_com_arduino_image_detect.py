import cv2
import torch
import pyautogui
import numpy as np
import serial
import time
from PIL import ImageGrab
from ultralytics import YOLO

# Configurer la communication série avec l'Arduino
port = 'COM10'  # Remplacez par le port COM correct (COMx sur Windows, /dev/ttyUSBx sur Linux)
baudrate = 9600
arduino = serial.Serial(port, baudrate, timeout=1)

# Charger le modèle YOLOv5 (modèle pré-entraîné ou modèle personnalisé .pt)
def load_yolov5_model(model_path='best_fornite.pt'):
    #mod = 'best.pt'
    #model = YOLO(mod)
    model = torch.hub.load('ultralytics/yolov5', 'custom', force_reload=True, path=model_path)  # Utilise un modèle personnalisé .pt
    model.eval()  # Mode évaluation
    return model

# Fonction pour la détection des objets dans l'image
def detect_objects(frame, model):
    results = model(frame)  # Passer l'image dans le modèle YOLOv5
    predictions = results.pred[0]  # Prédictions
    detected_objects = []

    # Extraire les coordonnées de la boîte englobante et les étiquettes
    for *xyxy, conf, cls in predictions:
        label = results.names[int(cls)]
        confidence = conf.item()
        xmin, ymin, xmax, ymax = map(int, xyxy)
        detected_objects.append((label, confidence, xmin, ymin, xmax, ymax))
        # Dessiner la boîte et le label sur l'image
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
        cv2.putText(frame, f'{label} {confidence:.2f}', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    return frame, detected_objects

# Fonction pour déplacer la souris en fonction des coordonnées de l'objet
def move_mouse(detected_objects, screen_width, screen_height):
    if detected_objects:
        # Prendre les coordonnées du premier objet détecté (ou le plus pertinent)
        _, _, xmin, ymin, xmax, ymax = detected_objects[0]
        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2
        
        # Mapper ces coordonnées à la résolution de l'écran
        mouse_x = int(center_x * screen_width / 1920)
        mouse_y = int(center_y * screen_height / 1080)
        
        # Déplacer la souris via PyAutoGUI
        pyautogui.moveTo(mouse_x, mouse_y)
        print(f"Moved mouse to: ({mouse_x}, {mouse_y})")

        # Envoyer les coordonnées à l'Arduino pour d'autres actions
        send_coordinates_to_arduino(mouse_x, mouse_y)

# Fonction pour envoyer les coordonnées à l'Arduino via le port COM
def send_coordinates_to_arduino(x, y):
    coordinates = f"{x},{y}\n"
    arduino.write(coordinates.encode())
    print(f"Sent coordinates to Arduino: {coordinates}")

# Fonction principale pour capturer l'écran, détecter les objets et déplacer la souris
def main():
    model = load_yolov5_model('best_fornite.pt')  # Charger votre modèle personnalisé
    screen_width, screen_height = pyautogui.size()  # Récupérer la taille de l'écran
    
    while True:
        # Capturer une image de l'écran
        screen = np.array(ImageGrab.grab())  # Capture l'écran
        frame = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)  # Convertir l'image au format RGB
        
        # Détection d'objets avec YOLOv5
        frame, detected_objects = detect_objects(frame, model)
        
        # Déplacer la souris en fonction de l'objet détecté
        move_mouse(detected_objects, screen_width, screen_height)

        # Afficher l'image avec les objets détectés
        cv2.imshow("YOLOv5 Object Detection", frame)

        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('o'):
            break

    # Fermer la caméra et la communication avec l'Arduino
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()