#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time

# ============================================
# FONCTION DE TRAITEMENT ORB
# ============================================

def ORB_detector(input_image, stored_image):
    """Compare l'image en direct avec l'image de référence."""
    # Conversion en gris pour le calcul
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # --- CORRECTION 1 : Utilisation de ORB_create ---
    # nfeatures=1600, scaleFactor=1.3
    orb_detector = cv2.ORB_create(nfeatures=1600, scaleFactor=1.3)

    # Détection et calcul des descripteurs
    (kp1, des1) = orb_detector.detectAndCompute(gray, None)
    (kp2, des2) = orb_detector.detectAndCompute(stored_image, None)

    # Si aucun point n'est trouvé, on évite le crash du matcher
    if des1 is None or des2 is None:
        return 0

    # Matcher Brute-Force avec Distance de Hamming
    # La distance de Hamming se calcule par : $d(a, b) = \sum (a_i \oplus b_i)$
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Tri par distance (les plus proches en premier)
    matches = sorted(matches, key=lambda x: x.distance)

    return len(matches)

# ============================================
# LOGIQUE DE DÉTECTION (COMMUNE)
# ============================================

def process_frame(frame, stored_image):
    """Applique la logique de zone et de détection sur une frame."""
    
    # --- CORRECTION 2 : Flip au tout début pour ne pas inverser le texte ---
    frame = cv2.flip(frame, 1)
    
    h, w = frame.shape[:2]

    # Définition de la ROI (Region of Interest) au centre
    # On utilise des entiers pour les coordonnées de pixels
    x1, y1 = int(w / 3), int((h / 2) + (h / 4))
    x2, y2 = int((w / 3) * 2), int((h / 2) - (h / 4))

    # Dessin du rectangle de visée (Rouge par défaut)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

    # Découpage de la zone pour ORB
    # Attention à l'ordre [y_start:y_end, x_start:x_end]
    roi = frame[y2:y1, x1:x2]

    # Calcul des correspondances
    num_matches = ORB_detector(roi, stored_image)

    # Affichage du score
    cv2.putText(frame, f"Matches: {num_matches}", (50, h - 50), 
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    # Seuil de détection
    threshold = 400
    if num_matches > threshold:
        # Rectangle Vert et message de succès
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(frame, "OBJET DETECTE !", (w // 4, 100), 
                    cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 2)
    
    return frame

# ============================================
# VERSIONS DE CAPTURE
# ============================================

def detection_standard():
    cap = cv2.VideoCapture(0)
    img_ref = cv2.imread('raspberry_pi.jpg', 0)
    
    if img_ref is None:
        print("Erreur : Fichier 'raspberry_pi.jpg' manquant.")
        return

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = process_frame(frame, img_ref)
        cv2.imshow('ORB Detection', frame)
        
        if cv2.waitKey(1) == 27: break
        
    cap.release()
    cv2.destroyAllWindows()

def detection_pi5():
    from picamera2 import Picamera2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "BGR888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    
    img_ref = cv2.imread('raspberry_pi.jpg', 0)
    
    try:
        while True:
            # Capture directe en BGR pour OpenCV
            frame = picam2.capture_array()
            frame = process_frame(frame, img_ref)
            cv2.imshow('ORB Detection Pi5', frame)
            if cv2.waitKey(1) == 27: break
    finally:
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        import picamera2
        print("Mode Raspberry Pi 5 activé.")
        detection_pi5()
    except ImportError:
        print("Mode PC/USB activé.")
        detection_standard()
