#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5.2 - Détection de Voitures dans une Vidéo
Détection de voitures en temps réel dans un flux vidéo

IMPORTANT - Pourquoi on utilise picamera2 au lieu de cv2.VideoCapture ?
---------------------------------------------------------------------------
Sur Raspberry Pi 5 avec caméra CSI, cv2.VideoCapture(0) ne fonctionne PAS
à cause d'un bug avec le backend GStreamer. La solution est d'utiliser
picamera2 pour capturer, puis OpenCV pour le traitement d'image.

Ce script propose deux versions :
- Version A : cv2.VideoCapture (PC / Webcam USB)
- Version B : picamera2 (Raspberry Pi 5 + Caméra CSI)
"""

import cv2
import time

# ============================================================================
# VERSION A : PC / WEBCAM USB (cv2.VideoCapture)
# ============================================================================

def detection_voitures_video_standard():
    """
    Version standard pour PC avec webcam USB ou fichier vidéo.
    Utilise cv2.VideoCapture qui fonctionne sur la plupart des plateformes.
    """
    # Chargement du classificateur Haar Cascade pour les voitures
    # Le fichier XML doit être dans le même dossier que le script
    cars_detect = cv2.CascadeClassifier('haarcascade_car.xml')
    
    # Vérifier que le classificateur a bien été chargé
    if cars_detect.empty():
        raise IOError("Impossible de charger haarcascade_car.xml")
    
    # Ouverture de la source vidéo
    # 'cars.avi' = fichier vidéo préenregistré
    # 0 = webcam par défaut (à remplacer par 0, 1, 2... selon votre config)
    capture = cv2.VideoCapture('cars.avi')
    
    # Vérifier que la vidéo a été ouverte
    if not capture.isOpened():
        raise IOError("Impossible d'ouvrir la vidéo cars.avi")
    
    print("Démarrage de la détection... Appuyez sur ESC pour quitter")
    
    # Boucle principale : traitement frame par frame
    while capture.isOpened():
        # Pause pour ralentir la lecture vidéo
        # Sans cela, la vidéo défile trop vite sur les machines rapides
        time.sleep(0.05)  # 50ms = ~20 FPS
        
        # Lecture d'une frame
        ret, frame = capture.read()
        
        # Vérifier que la lecture a réussi
        if not ret:
            print("Fin de la vidéo ou erreur de lecture")
            break
        
        # Conversion en niveaux de gris (requis pour Haar Cascade)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Détection des voitures
        # scaleFactor=1.4 : compensate for differing car sizes
        # minNeighbors=2 : plus permissif que pour les visages
        cars = cars_detect.detectMultiScale(gray, 1.4, 2)
        
        # Dessiner un rectangle bleu autour de chaque voiture détectée
        for (x, y, w, h) in cars:
            # (x, y) = coin supérieur gauche
            # (x+w, y+h) = coin inférieur droit
            # (255, 0, 0) = couleur bleue en BGR
            # 3 = épaisseur du trait en pixels
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
            
            # Optionnel : afficher les coordonnées
            # cv2.putText(frame, f'Car', (x, y-10), 
            #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
        
        # Affichage du résultat
        cv2.imshow('Voitures détectées', frame)
        
        # Sortie si touche ESC (code 27) pressée
        if cv2.waitKey(1) == 27:
            break
    
    # Libération des ressources
    capture.release()
    cv2.destroyAllWindows()
    print("Détection arrêtée")


# ============================================================================
# VERSION B : RASPBERRY PI 5 + CAMÉRA CSI (picamera2)
# ============================================================================

def detection_voitures_picamera2():
    """
    Version pour Raspberry Pi 5 avec caméra CSI.
    Utilise picamera2 pour la capture car cv2.VideoCapture(0) ne fonctionne pas.
    
    IMPORTANT : picamera2 capture en RGB, OpenCV travaille en BGR.
    Conversion nécessaire : cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    """
    from picamera2 import Picamera2
    
    # Chargement du classificateur Haar Cascade pour les voitures
    cars_detect = cv2.CascadeClassifier('haarcascade_car.xml')
    
    # Vérifier que le classificateur a bien été chargé
    if cars_detect.empty():
        raise IOError("Impossible de charger haarcascade_car.xml")
    
    # Initialisation de picamera2
    print("Initialisation de la caméra...")
    picam2 = Picamera2()
    
    # Configuration de la caméra
    # - format "RGB888" : 8 bits par canal Rouge, Vert, Bleu
    # - size (640, 480) : résolution VGA (rapide et suffisante)
    config = picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
    picam2.configure(config)
    
    # Démarrage de la caméra
    picam2.start()
    
    # Pause pour laisser la caméra s'initialiser (autofocus, exposition...)
    time.sleep(0.1)
    
    print("Démarrage de la détection... Appuyez sur ESC pour quitter")
    
    try:
        # Boucle principale
        while True:
            # Capture d'une image avec picamera2
            # Retourne un tableau NumPy au format RGB
            frame = picam2.capture_array()
            
            # CONVERSION OBLIGATOIRE : RGB → BGR
            # OpenCV utilise le format BGR par défaut
            # Sans cette conversion, les couleurs seront inversées (rouge ↔ bleu)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Conversion en niveaux de gris pour la détection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Détection des voitures
            cars = cars_detect.detectMultiScale(gray, 1.4, 2)
            
            # Dessiner les rectangles
            for (x, y, w, h) in cars:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
            
            # Affichage
            cv2.imshow('Voitures détectées', frame)
            
            # Sortie si ESC pressée
            if cv2.waitKey(1) == 27:
                break
    
    finally:
        # IMPORTANT : toujours arrêter proprement la caméra
        # Même en cas d'erreur (d'où le try/finally)
        picam2.stop()
        cv2.destroyAllWindows()
        print("Détection arrêtée, caméra libérée")


# ============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    """
    Choisissez la version à exécuter selon votre configuration :
    
    - PC avec webcam USB ou fichier vidéo : utilisez detection_voitures_video_standard()
    - Raspberry Pi 5 + Caméra CSI : utilisez detection_voitures_picamera2()
    
    Par défaut, la version standard est exécutée.
    """
    
    import sys
    
    # Détection automatique ou choix manuel
    try:
        # Essayer d'importer picamera2 (disponible uniquement sur Raspberry Pi)
        from picamera2 import Picamera2
        
        # Vérifier si on est sur Raspberry Pi en cherchant le module caméra
        import os
        if os.path.exists('/dev/video0'):
            print("Caméra détectée sur /dev/video0")
        
        # Par défaut, utiliser picamera2 sur Raspberry Pi
        print("Picamera2 détecté - utilisation de la version Raspberry Pi")
        detection_voitures_picamera2()
        
    except ImportError:
        # picamera2 non installé = on est probablement sur PC
        print("Picamera2 non détecté - utilisation de la version standard (PC/Webcam)")
        detection_voitures_video_standard()
