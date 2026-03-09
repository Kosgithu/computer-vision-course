#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5.4 - Détection Temps Réel avec ORB
=====================================
Reconnaissance d'objets en temps réel avec ORB (Oriented FAST and Rotated BRIEF)

IMPORTANT - Pourquoi on utilise picamera2 sur Raspberry Pi 5 ?
---------------------------------------------------------------
Sur Raspberry Pi 5 avec caméra CSI, cv2.VideoCapture(0) ne fonctionne PAS
à cause d'un bug avec le backend GStreamer. La solution est d'utiliser
picamera2 pour capturer, puis OpenCV pour le traitement d'image.
"""

import cv2
import numpy as np


# ============================================
# VERSION STANDARD - PC avec Webcam USB
# ============================================

def ORB(input_image, stored_image):
    """
    Cette fonction compare l'image capturée par la webcam avec l'image stockée.
    La fonction ORB retourne le nombre de correspondances entre les deux images.
    
    ORB = Oriented FAST and Rotated BRIEF
    - FAST : Features from Accelerated Segment Test (détecte les points clés)
    - BRIEF : Binary Robust Independent Elementary Features (décrit les points)
    
    FAST trouve les points d'intérêt (keypoints)
    Les descripteurs sont des vecteurs qui stockent l'information sur les points clés
    BRIEF est une méthode rapide pour calculer et matcher les descripteurs
    ORB = Fusion du détecteur FAST + descripteur BRIEF
    """
    
    # Conversion RGB vers niveaux de gris avec la fonction cv2.COLOR_BGR2GRAY
    # BGR (les bytes sont inversés par rapport à RGB)
    # cv2.cvtColor : Convertit une image d'un espace colorimétrique à un autre
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # cv2.ORB est la fonction intégrée utilisée pour la détection d'objets
    # cv2.ORB(keypoints, facteur_de_mise_à_léchelle)
    # 1600 = nombre maximum de points clés, 1.3 = facteur de mise à l'échelle
    orb_detector = cv2.ORB(1600, 1.3)

    # Détection des points clés sur l'image d'entrée après conversion en gris
    # avec cv2.ORB.detectAndCompute
    # cv2.ORB.detectAndCompute(image_grise, masque)
    (keypoints_1, descriptor_1) = orb_detector.detectAndCompute(gray, None)

    # Détection des points clés sur l'image stockée
    # cv2.ORB.detectAndCompute(image_stockée, masque)
    (keypoints_2, descriptor_2) = orb_detector.detectAndCompute(stored_image, None)

    # Le Brute-Force Matcher est utilisé pour matcher les caractéristiques entre 2 images
    # cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck)
    
    # cv2.NORM_HAMMING utilise la distance de Hamming comme mesure
    # La distance de Hamming = nombre de positions où les bits correspondants sont différents
    
    # crossCheck=False par défaut
    # True indique que 2 caractéristiques dans l'image d'entrée et l'image stockée se correspondent
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Matcher les deux descripteurs avec la fonction cv2.BFMatcher.match
    # cv2.BFMatcher.match(descripteur_1, descripteur_2)
    matches_found = brute_force.match(descriptor_1, descriptor_2)

    # Les correspondances trouvées sont triées par distance, la plus petite distance est la meilleure
    # sorted(liste, clé)
    matches_found = sorted(matches_found, key=lambda val: val.distance)

    return len(matches_found)


def detection_orb_standard():
    """Version standard pour PC avec webcam USB."""
    
    # Initialisation de l'objet de capture vidéo
    capture = cv2.VideoCapture(0)
    # Une caméra est connectée en passant 0 OU -1
    # Une deuxième caméra peut être sélectionnée en passant 2

    # Chargement de l'image stockée en niveaux de gris
    # L'image 'raspberry_pi.jpg' doit être présente dans le dossier
    stored_image = cv2.imread('raspberry_pi.jpg', 0)
    
    if stored_image is None:
        print("Erreur : Image 'raspberry_pi.jpg' non trouvée!")
        print("Placez une image nommée 'raspberry_pi.jpg' dans le dossier courant.")
        return

    while True:
        # Début de la capture des frames
        ret, capturing = capture.read()
        
        if not ret:
            break

        # La hauteur et la largeur des frames sont récupérées
        frame_height, frame_width = capturing.shape[:2]

        # Définition des dimensions de la boîte au centre de la frame
        x1_top_left = frame_width / 3
        y1_top_left = (frame_height / 2) + (frame_height / 4)
        x2_bottom_right = (frame_width / 3) * 2
        y2_bottom_right = (frame_height / 2) - (frame_height / 4)

        # Dessin d'un rectangle autour des dimensions définies avec cv2.rectangle
        # cv2.rectangle(image, (x1,y1), (x2,y2), couleur, épaisseur)
        cv2.rectangle(capturing, (int(x1_top_left), int(y1_top_left)), 
                      (int(x2_bottom_right), int(y2_bottom_right)), (0, 0, 255), 4)

        # La région définie par le rectangle est rognée (crop)
        cropped_box = capturing[int(y2_bottom_right):int(y1_top_left), 
                                int(x1_top_left):int(x2_bottom_right)]

        # La frame capturée est retournée horizontalement avec cv2.flip
        # Retournement horizontal avec la valeur '1'
        capturing = cv2.flip(capturing, 1)

        # La fonction ORB est appelée pour trouver les correspondances
        matches_found = ORB(cropped_box, stored_image)

        # Les correspondances trouvées sont affichées en texte
        string = "Matches Found = " + str(matches_found)
        # Pour afficher une chaîne de texte, cv2.putText est utilisé
        # cv2.putText(image, texte, origine, police, taillePolice, couleur, épaisseur)
        cv2.putText(capturing, string, (150, 400), cv2.FONT_HERSHEY_COMPLEX, 
                    1, (0, 0, 255), 2)

        # Définition du seuil selon l'image stockée pour indiquer la détection d'objet
        # Pour de nouvelles images ou conditions d'éclairage, vous devrez expérimenter
        set_threshold = 400
        # Le détecteur ORB récupère les 1600 meilleures correspondances,
        # un seuil de 400 indique qu'au moins 25% doivent correspondre

        # Quand les correspondances dépassent le seuil, l'objet est détecté
        if matches_found > set_threshold:
            
            # Le rectangle est dessiné en vert après détection de l'objet
            # cv2.rectangle(image, (x1,y1), (x2,y2), couleur, épaisseur)
            cv2.rectangle(capturing, (int(x1_top_left), int(y1_top_left)), 
                          (int(x2_bottom_right), int(y2_bottom_right)), (0, 255, 0), 4)

            # Affichage du texte "Object Detected"
            # cv2.putText(image, texte, origine, police, taillePolice, couleur, épaisseur)
            cv2.putText(capturing, 'Object Detected', (200, 50), 
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

        # Affichage de la détection d'objet avec la fonction imshow
        cv2.imshow('Real-time Object Detection', capturing)

        # Vérification si l'utilisateur a appuyé sur la touche Esc
        c = cv2.waitKey(1)
        if c == 27:
            break

    # Fermeture du périphérique de capture
    capture.release()

    # Fermeture de toutes les fenêtres
    cv2.destroyAllWindows()


# ============================================
# VERSION RASPBERRY PI 5 - Caméra CSI
# ============================================

def detection_orb_picamera2():
    """Version pour Raspberry Pi 5 avec caméra CSI (utilise picamera2)."""
    from picamera2 import Picamera2
    import time
    
    # Initialisation de picamera2
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    ))
    picam2.start()
    time.sleep(0.1)  # Délai pour laisser la caméra s'initialiser

    # Chargement de l'image stockée en niveaux de gris
    stored_image = cv2.imread('raspberry_pi.jpg', 0)
    
    if stored_image is None:
        print("Erreur : Image 'raspberry_pi.jpg' non trouvée!")
        print("Placez une image nommée 'raspberry_pi.jpg' dans le dossier courant.")
        picam2.stop()
        return

    print("Démarrage ORB... Appuyez sur ESC pour quitter")

    try:
        while True:
            # Capture avec picamera2 (format RGB)
            capturing = picam2.capture_array()
            
            # Conversion RGB → BGR (obligatoire pour OpenCV)
            capturing = cv2.cvtColor(capturing, cv2.COLOR_RGB2BGR)

            # La hauteur et la largeur des frames sont récupérées
            frame_height, frame_width = capturing.shape[:2]

            # Définition des dimensions de la boîte au centre de la frame
            x1_top_left = frame_width / 3
            y1_top_left = (frame_height / 2) + (frame_height / 4)
            x2_bottom_right = (frame_width / 3) * 2
            y2_bottom_right = (frame_height / 2) - (frame_height / 4)

            # Dessin d'un rectangle autour des dimensions définies
            cv2.rectangle(capturing, (int(x1_top_left), int(y1_top_left)), 
                          (int(x2_bottom_right), int(y2_bottom_right)), (0, 0, 255), 4)

            # La région définie par le rectangle est rognée (crop)
            cropped_box = capturing[int(y2_bottom_right):int(y1_top_left), 
                                    int(x1_top_left):int(x2_bottom_right)]

            # La frame capturée est retournée horizontalement
            capturing = cv2.flip(capturing, 1)

            # La fonction ORB est appelée pour trouver les correspondances
            matches_found = ORB(cropped_box, stored_image)

            # Les correspondances trouvées sont affichées en texte
            string = "Matches Found = " + str(matches_found)
            cv2.putText(capturing, string, (150, 400), cv2.FONT_HERSHEY_COMPLEX, 
                        1, (0, 0, 255), 2)

            # Définition du seuil
            set_threshold = 400

            # Quand les correspondances dépassent le seuil, l'objet est détecté
            if matches_found > set_threshold:
                cv2.rectangle(capturing, (int(x1_top_left), int(y1_top_left)), 
                              (int(x2_bottom_right), int(y2_bottom_right)), (0, 255, 0), 4)
                cv2.putText(capturing, 'Object Detected', (200, 50), 
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            # Affichage de la détection
            cv2.imshow('Real-time Object Detection', capturing)

            # Vérification si l'utilisateur a appuyé sur la touche Esc
            c = cv2.waitKey(1)
            if c == 27:
                break
    
    finally:
        # Arrêt propre de picamera2
        picam2.stop()
        cv2.destroyAllWindows()


# ============================================
# POINT D'ENTRÉE
# ============================================

if __name__ == "__main__":
    # Détection automatique : picamera2 si disponible (Raspberry Pi), sinon VideoCapture
    try:
        from picamera2 import Picamera2
        print("Picamera2 détecté - utilisation du mode Raspberry Pi")
        detection_orb_picamera2()
    except ImportError:
        print("Picamera2 non détecté - utilisation du mode standard (Webcam)")
        detection_orb_standard()
