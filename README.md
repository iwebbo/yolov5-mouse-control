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
   python yolov5_arduino_control.py
   ```

2. Le programme capturera l'écran en temps réel, détectera des objets, et déplacera la souris en conséquence.

3. Pour arrêter le script, appuyez sur la touche `o`.

## Fonctionnalités

- **Détection d'objets en temps réel** : Utilise YOLOv5 pour identifier les objets à l'écran.
- **Contrôle de la souris** : Déplace la souris vers le centre de l'objet détecté.
- **Communication avec Arduino** : Envoie les coordonnées des objets détectés via le port série.

## Limitations

- La détection est limitée par les performances du modèle YOLOv5 et la vitesse de capture de l'écran.
- Assurez-vous que la résolution de l'écran utilisée dans le jeu correspond à celle configurée dans le script (par défaut : 1920x1080).

## Dépannage

- Si la souris ne bouge pas correctement, vérifiez que les coordonnées de l'écran et les paramètres de résolution sont corrects.
- Assurez-vous que l'Arduino est connecté au bon port série et que le baudrate correspond.
