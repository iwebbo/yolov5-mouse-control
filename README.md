# Contrôle de Souris Automatisé avec YOLOv5 et Arduino

Ce projet utilise un modèle YOLOv5 personnalisé pour détecter des objets à l'écran et contrôler la position de la souris en fonction des objets détectés. Il envoie également les coordonnées des objets détectés à un Arduino via une communication série.

## Prérequis

### Matériel :
- Un ordinateur capable de capturer l'écran en temps réel.
- Un Arduino connecté via un port série (par exemple, Arduino Uno).
- Un câble USB pour la connexion entre l'ordinateur et l'Arduino.

### Logiciel :
- Python 3.x installé sur votre machine.
- Bibliothèques Python nécessaires (voir [Installation](#installation)).
- Un modèle YOLOv5 personnalisé au format `.pt` (par exemple, `best_fornite.pt`).

## Installation

1. Installez les bibliothèques Python requises :
   ```bash
   pip install opencv-python torch pyautogui numpy pillow ultralytics
   ```

2. Connectez votre Arduino et notez le port série utilisé (par exemple, `COM10` sous Windows ou `/dev/ttyUSBx` sous Linux).

3. Téléchargez ou entraînez votre propre modèle YOLOv5, puis placez-le dans le répertoire du projet.

## Configuration

- **Port série Arduino** : Modifiez la variable `port` dans le script pour correspondre au port série de votre Arduino.
- **Modèle YOLOv5** : Assurez-vous que le fichier modèle spécifié dans `load_yolov5_model()` correspond au chemin de votre modèle personnalisé (par défaut : `best_fornite.pt`).

## Utilisation

1. Lancez le script Python :
   ```bash
   python mousecontrol_for_com_arduino_image_detect.py
   ```

2. Le programme capturera l'écran en temps réel, détectera des objets, et déplacera la souris en conséquence.

3. Ne pas oublier de modifier ces valeurs en fonction de vos entrées computer.
4. port = 'COM10'  # Remplacez par le port COM correct (COMx sur Windows, /dev/ttyUSBx sur Linux)
5. baudrate = 9600 # A modifier en fonction de votre input arduino, à modifier également si des latences sont perçus, afin de ne pas surchager l'arduino.
6. def load_yolov5_model(model_path='best_fornite.pt'): # Modifier par votre modele, dans ce cas présent, nous avons entrainés depuis un dataset custom Fortnite, au sein du Repo utiliser 326_head_body.pt

## Fonctionnalités

- **Détection d'objets en temps réel** : Utilise YOLOv5 pour identifier les objets à l'écran.
- **Contrôle de la souris** : Déplace la souris vers le centre de l'objet détecté.
- **Communication avec Arduino** : Envoie les coordonnées des objets détectés via le port série.

## Limitations

- La détection est limitée par les performances du modèle YOLOv5 et la vitesse de capture de l'écran.
- Le projet devrait être migré en Yolov8 & Yolov11 (https://github.com/iwebbo/yolov8-tracking-fps)
- Assurez-vous que la résolution de l'écran utilisée dans le jeu correspond à celle configurée dans le script (par défaut : 1920x1080).

## Dépannage

- Si la souris ne bouge pas correctement, vérifiez votre modèle & le prompt est resté en verbose, vous aurez donc accès aux logs.
- Assurez-vous que l'Arduino est connecté au bon port série et que le baudrate correspond.
- Assurez-vous que le firmware est correctement chargé sur votre arduino.
- Assusez-vous que votre résolution soit coordonnnée : # Mapper ces coordonnées à la résolution de l'écran
