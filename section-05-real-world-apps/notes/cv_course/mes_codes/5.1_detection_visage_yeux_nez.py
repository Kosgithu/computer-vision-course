#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5.1 - Détection Temps Réel : Visage, Yeux et Nez
Real-time Human Face, Eyes and Nose Detection

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
import numpy as np
import time

# ============================================================================
# VERSION A : PC / WEBCAM USB (cv2.VideoCapture)
# ============================================================================

def detection_visage_yeux_nez_standard():
    """
    Version standard pour PC avec webcam USB.
    Détection temps réel de visages, yeux et nez.
    """
    # ═══════════════════════════════════════════════════════════════
    # CHARGEMENT DES CLASSIFICATEURS HAAR CASCADE
    # ═══════════════════════════════════════════════════════════════
    
    # Charge le fichier cascade pour la détection de visage
    face_detect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    
    # Charge le fichier cascade pour la détection des yeux
    eyes_detect = cv2.CascadeClassifier('haarcascade_eye.xml')
    
    # Charge le fichier cascade pour la détection du nez
    # Note : "mcs_nose" dans le nom du fichier
    nose_detect = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
    
    # ───────────────────────────────────────────────────────────────
    # VÉRIFICATION DU CHARGEMENT DES FICHIERS
    # ───────────────────────────────────────────────────────────────
    
    if face_detect.empty():
        raise IOError('Impossible de charger haarcascade_frontalface_alt.xml')
    if eyes_detect.empty():
        raise IOError('Impossible de charger haarcascade_eye.xml')
    if nose_detect.empty():
        raise IOError('Impossible de charger haarcascade_mcs_nose.xml')
    
    # ═══════════════════════════════════════════════════════════════
    # INITIALISATION DE LA CAPTURE VIDÉO
    # ═══════════════════════════════════════════════════════════════
    
    capture = cv2.VideoCapture(0)
    # Paramètres possibles :
    #   0 ou -1  → Caméra par défaut
    #   1, 2...  → Autres caméras
    #   'fichier.avi' → Fichier vidéo
    
    # ═══════════════════════════════════════════════════════════════
    # BOUCLE PRINCIPALE
    # ═══════════════════════════════════════════════════════════════
    
    print("Démarrage de la détection... Appuyez sur ESC pour quitter")
    
    while True:
        # Lecture d'une frame
        ret, capturing = capture.read()
        
        if not ret:
            print("Erreur de lecture de la caméra")
            break
        
        # Redimensionnement pour accélérer le traitement
        resize_frame = cv2.resize(capturing, None, fx=0.5, fy=0.5, 
                interpolation=cv2.INTER_AREA)
        
        # Conversion en niveaux de gris
        gray = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)
        
        # Détection des visages
        face_detection = face_detect.detectMultiScale(gray, 1.3, 5)
        
        # Traitement de chaque visage
        for (x, y, w, h) in face_detection:
            # Rectangle rouge autour du visage
            cv2.rectangle(resize_frame, (x, y), (x+w, y+h), (0,0,255), 10)
            
            # Extraction de la ROI
            gray_roi = gray[y:y+h, x:x+w]
            color_roi = resize_frame[y:y+h, x:x+w]
            
            # Détection des yeux (bleu)
            eye_detector = eyes_detect.detectMultiScale(gray_roi)
            for (eye_x, eye_y, eye_w, eye_h) in eye_detector:
                cv2.rectangle(color_roi, 
                             (eye_x, eye_y), 
                             (eye_x + eye_w, eye_y + eye_h),
                             (255, 0, 0), 5)
            
            # Détection du nez (vert)
            nose_detector = nose_detect.detectMultiScale(gray_roi, 1.3, 5)
            for (nose_x, nose_y, nose_w, nose_h) in nose_detector:
                cv2.rectangle(color_roi, 
                             (nose_x, nose_y), 
                             (nose_x + nose_w, nose_y + nose_h),
                             (0, 255, 0), 5)
        
        # Affichage
        cv2.imshow("Detection Temps Reel", resize_frame)
        
        # Quitter avec ESC
        if cv2.waitKey(1) == 27:
            break
    
    # Nettoyage
    capture.release()
    cv2.destroyAllWindows()
    print("Détection arrêtée")


# ============================================================================
# VERSION B : RASPBERRY PI 5 + CAMÉRA CSI (picamera2)
# ============================================================================

def detection_visage_yeux_nez_picamera2():
    """
    Version pour Raspberry Pi 5 avec caméra CSI.
    Utilise picamera2 pour la capture car cv2.VideoCapture(0) ne fonctionne pas.
    """
    from picamera2 import Picamera2
    
    # ═══════════════════════════════════════════════════════════════
    # CHARGEMENT DES CLASSIFICATEURS
    # ═══════════════════════════════════════════════════════════════
    
    face_detect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    eyes_detect = cv2.CascadeClassifier('haarcascade_eye.xml')
    nose_detect = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
    
    if face_detect.empty():
        raise IOError('Impossible de charger haarcascade_frontalface_alt.xml')
    if eyes_detect.empty():
        raise IOError('Impossible de charger haarcascade_eye.xml')
    if nose_detect.empty():
        raise IOError('Impossible de charger haarcascade_mcs_nose.xml')
    
    # ═══════════════════════════════════════════════════════════════
    # INITIALISATION PICAMERA2
    # ═══════════════════════════════════════════════════════════════
    
    print("Initialisation de la caméra...")
    picam2 = Picamera2()
    
    # Configuration : RGB888 pour avoir 3 canaux (RGB)
    # Pas besoin de redimensionner, on contrôle la résolution ici
    picam2.configure(picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    ))
    
    picam2.start()
    time.sleep(0.1)  # Laisser la caméra s'initialiser
    
    print("Démarrage de la détection... Appuyez sur ESC pour quitter")
    
    try:
        while True:
            # Capture avec picamera2 (format RGB)
            frame = picam2.capture_array()
            
            # CONVERSION OBLIGATOIRE : RGB → BGR
            # OpenCV travaille en BGR par défaut
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Redimensionnement pour accélérer
            resize_frame = cv2.resize(frame, None, fx=0.5, fy=0.5, 
                    interpolation=cv2.INTER_AREA)
            
            # Conversion en niveaux de gris
            gray = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)
            
            # Détection des visages
            face_detection = face_detect.detectMultiScale(gray, 1.3, 5)
            
            # Traitement de chaque visage
            for (x, y, w, h) in face_detection:
                # Rectangle rouge autour du visage
                cv2.rectangle(resize_frame, (x, y), (x+w, y+h), (0,0,255), 10)
                
                # Extraction de la ROI
                gray_roi = gray[y:y+h, x:x+w]
                color_roi = resize_frame[y:y+h, x:x+w]
                
                # Détection des yeux (bleu)
                eye_detector = eyes_detect.detectMultiScale(gray_roi)
                for (eye_x, eye_y, eye_w, eye_h) in eye_detector:
                    cv2.rectangle(color_roi, 
                                 (eye_x, eye_y), 
                                 (eye_x + eye_w, eye_y + eye_h),
                                 (255, 0, 0), 5)
                
                # Détection du nez (vert)
                nose_detector = nose_detect.detectMultiScale(gray_roi, 1.3, 5)
                for (nose_x, nose_y, nose_w, nose_h) in nose_detector:
                    cv2.rectangle(color_roi, 
                                 (nose_x, nose_y), 
                                 (nose_x + nose_w, nose_y + nose_h),
                                 (0, 255, 0), 5)
            
            # Affichage
            cv2.imshow("Detection Temps Reel", resize_frame)
            
            # Quitter avec ESC
            if cv2.waitKey(1) == 27:
                break
    
    finally:
        # IMPORTANT : toujours arrêter proprement
        picam2.stop()
        cv2.destroyAllWindows()
        print("Détection arrêtée")


# ============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    """
    Choix automatique de la version selon la plateforme.
    """
    try:
        from picamera2 import Picamera2
        print("Picamera2 détecté - utilisation de la version Raspberry Pi")
        detection_visage_yeux_nez_picamera2()
    except ImportError:
        print("Picamera2 non détecté - utilisation de la version standard")
        detection_visage_yeux_nez_standard()
