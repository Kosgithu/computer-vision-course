#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5.3 - Détection de Piétons (CCTV)
Détection de piétons en temps réel avec caméra de surveillance

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

def detection_pietons_standard():
    """
    Version standard pour PC avec webcam USB ou fichier vidéo.
    Détection de piétons avec classificateurs fullbody et upperbody.
    """
    # Chargement des classificateurs Haar Cascade
    body_detect = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    upperbody_detect = cv2.CascadeClassifier('haarcascade_upperbody.xml')
    
    # Vérifier que les classificateurs ont bien été chargés
    if body_detect.empty():
        raise IOError("Impossible de charger haarcascade_fullbody.xml")
    if upperbody_detect.empty():
        raise IOError("Impossible de charger haarcascade_upperbody.xml")
    
    # Ouverture de la source vidéo
    # 0 = webcam par défaut, ou remplacer par 'fichier.mp4'
    capture = cv2.VideoCapture(0)
    
    if not capture.isOpened():
        raise IOError("Impossible d'ouvrir la caméra")
    
    print("Démarrage de la détection CCTV... Appuyez sur ESC pour quitter")
    person_count = 0
    
    while capture.isOpened():
        ret, frame = capture.read()
        
        if not ret:
            print("Erreur de lecture ou fin de vidéo")
            break
        
        # Conversion en niveaux de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Détection corps entier
        bodies = body_detect.detectMultiScale(gray, 1.1, 3)
        
        # Détection haut du corps
        upper_bodies = upperbody_detect.detectMultiScale(gray, 1.1, 3)
        
        # Dessin des rectangles - corps entier (vert)
        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, 'Personne', (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Dessin des rectangles - haut du corps (bleu)
        for (x, y, w, h) in upper_bodies:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, 'Haut corps', (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Compteur de personnes
        total = len(bodies) + len(upper_bodies)
        if total != person_count:
            person_count = total
            if person_count > 0:
                print(f"Personnes détectées : {person_count}")
        
        cv2.putText(frame, f'Personnes: {person_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Affichage
        cv2.imshow('Détection Piétons CCTV', frame)
        
        if cv2.waitKey(1) == 27:  # ESC
            break
    
    capture.release()
    cv2.destroyAllWindows()
    print("Détection arrêtée")


# ============================================================================
# VERSION B : RASPBERRY PI 5 + CAMÉRA CSI (picamera2)
# ============================================================================

def detection_pietons_picamera2():
    """
    Version pour Raspberry Pi 5 avec caméra CSI.
    Utilise picamera2 pour la capture car cv2.VideoCapture(0) ne fonctionne pas.
    """
    from picamera2 import Picamera2
    
    # Chargement des classificateurs
    body_detect = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    upperbody_detect = cv2.CascadeClassifier('haarcascade_upperbody.xml')
    
    if body_detect.empty():
        raise IOError("Impossible de charger haarcascade_fullbody.xml")
    if upperbody_detect.empty():
        raise IOError("Impossible de charger haarcascade_upperbody.xml")
    
    # Initialisation picamera2
    print("Initialisation de la caméra...")
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    ))
    picam2.start()
    time.sleep(0.1)
    
    print("Démarrage de la détection CCTV... Appuyez sur ESC pour quitter")
    person_count = 0
    
    try:
        while True:
            # Capture avec picamera2 (format RGB)
            frame = picam2.capture_array()
            
            # CONVERSION OBLIGATOIRE : RGB → BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Conversion en niveaux de gris
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Détection corps entier
            bodies = body_detect.detectMultiScale(gray, 1.1, 3)
            
            # Détection haut du corps
            upper_bodies = upperbody_detect.detectMultiScale(gray, 1.1, 3)
            
            # Dessin des rectangles
            for (x, y, w, h) in bodies:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Personne', (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            for (x, y, w, h) in upper_bodies:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, 'Haut corps', (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            # Compteur
            total = len(bodies) + len(upper_bodies)
            if total != person_count:
                person_count = total
                if person_count > 0:
                    print(f"Personnes détectées : {person_count}")
            
            cv2.putText(frame, f'Personnes: {person_count}', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            # Affichage
            cv2.imshow('Détection Piétons CCTV', frame)
            
            if cv2.waitKey(1) == 27:  # ESC
                break
    
    finally:
        picam2.stop()
        cv2.destroyAllWindows()
        print("Détection arrêtée")


# ============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    """
    Choix automatique de la version selon la plateforme.
    - Si picamera2 est disponible → Raspberry Pi
    - Sinon → PC standard
    """
    try:
        from picamera2 import Picamera2
        print("Picamera2 détecté - utilisation de la version Raspberry Pi")
        detection_pietons_picamera2()
    except ImportError:
        print("Picamera2 non détecté - utilisation de la version standard")
        detection_pietons_standard()
