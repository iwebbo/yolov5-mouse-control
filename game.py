import cv2
import torch
import serial
import time

# Configurer la communication série avec l'Arduino
port = 'COM10'  # Remplacez par votre port COM
baudrate = 9600
arduino = serial.Serial(port, baudrate, timeout=1)

# Fonction d'envoi des données à l'Arduino
def send_data_to_arduino(data):
    arduino.write(data.encode())  # Envoie de données sous forme d'octets
    print(f"Data sent to Arduino: {data}")

# Fonction pour charger le modèle YOLOv5
def load_yolov5_model():
    # Charger le modèle pré-entraîné de YOLOv5 (légère version)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Vous pouvez choisir yolov5m, yolov5l, etc.
    model.eval()
    return model

# Fonction de détection avec YOLOv5
def detect_objects(frame, model):
    # Faire la prédiction avec YOLOv5
    results = model(frame)
    
    # Extraire les informations sur les objets détectés
    labels = results.names  # Liste des labels d'objets
    pred = results.pred[0]  # Les prédictions (boîtes, scores et classes)
    
    detected_objects = []
    
    for *xyxy, conf, cls in pred:
        label = labels[int(cls)]
        confidence = conf.item()
        detected_objects.append((label, confidence))
        
        # Dessiner les résultats sur l'image
        xmin, ymin, xmax, ymax = map(int, xyxy)
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
        cv2.putText(frame, f'{label} {confidence:.2f}', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    return frame, detected_objects

# Boucle principale pour traiter les images en temps réel
def main():
    model = load_yolov5_model()  # Charger le modèle YOLOv5
    cap = cv2.VideoCapture(0)  # Ouvrir la caméra (ou fichier vidéo)

    if not cap.isOpened():
        print("Erreur d'ouverture de la caméra.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Détection d'objets dans l'image
        frame, detected_objects = detect_objects(frame, model)

        # Afficher l'image avec les résultats de la détection
        cv2.imshow("YOLOv5 Detection", frame)

        # Envoyer les résultats à l'Arduino
        if detected_objects:
            # Par exemple, envoyer le premier objet détecté
            label, confidence = detected_objects[0]
            data_to_send = f"{label}:{confidence:.2f}\n"
            send_data_to_arduino(data_to_send)
        
        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()