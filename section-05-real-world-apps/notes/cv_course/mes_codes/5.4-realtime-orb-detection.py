#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time

# ============================================
# FONCTION DE TRAITEMENT ORB
# ============================================

def ORB_detector(input_image, stored_image):
    """
    Compare l'image en direct avec l'image de référence.
    ORB (Oriented FAST and Rotated BRIEF) est une alternative rapide et gratuite à SIFT.
    """
    # Conversion en niveaux de gris : ORB n'a pas besoin de la couleur pour calculer les contrastes
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # Initialisation du détecteur ORB
    # nfeatures : nombre de points d'intérêt à chercher (plus c'est haut, plus c'est précis mais lent)
    # scaleFactor : ratio de la pyramide d'images (pour détecter l'objet de loin ou de près)
    orb_detector = cv2.ORB_create(nfeatures=1600, scaleFactor=1.3)

    # detectAndCompute : Trouve les points clés (kp) et calcule leur "signature" numérique (des)
    (kp1, des1) = orb_detector.detectAndCompute(gray, None)
    (kp2, des2) = orb_detector.detectAndCompute(stored_image, None)

    # Sécurité : Si l'un des deux descripteurs est vide (ex: caméra cachée), on arrête pour éviter un crash
    if des1 is None or des2 is None:
        return 0

    # BFMatcher (Brute-Force) : Compare chaque point de l'image A avec chaque point de l'image B
    # NORM_HAMMING : La mesure mathématique adaptée aux descripteurs binaires d'ORB
    # Distance de Hamming : $$d(a, b) = \sum (a_i \oplus b_i)$$
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    # On cherche les correspondances (matches)
    matches = bf.match(des1, des2)

    # Tri des correspondances : on place les plus "sûres" (distance la plus courte) en début de liste
    matches = sorted(matches, key=lambda x: x.distance)

    return len(matches)

# ============================================
# LOGIQUE DE DÉTECTION (COMMUNE)
# ============================================

def process_frame(frame, stored_image):
    """
    Prépare l'image, définit la zone de scan et gère l'affichage visuel.
    """
    # Effet miroir : Inversion horizontale pour que la gauche de l'écran soit votre gauche
    # On le fait au début pour que le dessin et le texte ne soient pas inversés
    frame = cv2.flip(frame, 1)
    
    # Récupération des dimensions de l'image
    h, w = frame.shape[:2]

    # Définition de la ROI (Region of Interest) : un rectangle au centre de l'écran
    # x1, y1 : coin inférieur gauche | x2, y2 : coin supérieur droit
    x1, y1 = int(w / 3), int((h / 2) + (h / 4))
    x2, y2 = int((w / 3) * 2), int((h / 2) - (h / 4))

    # Dessin du rectangle de visée (Rouge par défaut)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

    # Découpage (Crop) de la zone à analyser pour ne pas gaspiller de puissance sur le décor
    # Rappel NumPy : l'ordre est [y_début:y_fin, x_début:x_fin]
    roi = frame[y2:y1, x1:x2]

    # On envoie la petite zone découpée au détecteur ORB
    num_matches = ORB_detector(roi, stored_image)

    # Affichage du score de points communs en bas de l'image
    cv2.putText(frame, f"Matches: {num_matches}", (50, h - 50), 
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    # Seuil de détection (Threshold) : Ajustez cette valeur selon la difficulté
    threshold = 400
    if num_matches > threshold:
        # Si le seuil est dépassé, on change le rectangle en Vert et on affiche un message
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(frame, "OBJET DETECTE !", (w // 4, 100), 
                    cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 2)
    
    return frame

# ============================================
# VERSIONS DE CAPTURE
# ============================================

def detection_standard():
    """Utilise la Webcam USB standard via OpenCV."""
    cap = cv2.VideoCapture(0)
    img_ref = cv2.imread('raspberry_pi.jpg', 0) # Charge l'image cible en gris
    
    if img_ref is None:
        print("Erreur : Fichier 'raspberry_pi.jpg' introuvable dans le dossier.")
        return

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # Traitement de l'image
        frame = process_frame(frame, img_ref)
        cv2.imshow('ORB Detection - PC', frame)
        
        # Sortie avec la touche ESC (code 27)
        if cv2.waitKey(1) == 27: break
        
    cap.release()
    cv2.destroyAllWindows()

def detection_pi5():
    """Utilise la caméra CSI du Raspberry Pi 5 via Picamera2."""
    from picamera2 import Picamera2
    
    # Configuration spécifique à la caméra du Pi 5
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": "BGR888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    
    img_ref = cv2.imread('raspberry_pi.jpg', 0)
    
    try:
        while True:
            # Capture de l'image sous forme de tableau NumPy
            frame = picam2.capture_array()
            frame = process_frame(frame, img_ref)
            cv2.imshow('ORB Detection - Pi5', frame)
            
            if cv2.waitKey(1) == 27: break
    finally:
        # Fermeture propre pour libérer la caméra
        picam2.stop()
        cv2.destroyAllWindows()

# ============================================
# DÉMARRAGE AUTOMATIQUE
# ============================================

if __name__ == "__main__":
    try:
        # Si picamera2 est installé, on est probablement sur un Raspberry Pi
        import picamera2
        print("Environnement Raspberry Pi détecté.")
        detection_pi5()
    except ImportError:
        # Sinon, on utilise la webcam classique
        print("Environnement PC/Webcam détecté.")
        detection_standard()
"""Les 6 étapes clés du code :
Initialisation (La mémoire) : Le programme charge en mémoire l'image de l'objet que tu veux reconnaître (ex: raspberry_pi.jpg). Il calcule une fois pour toutes ses points de repère.

Capture & Miroir : Il récupère l'image de la caméra. Il l'inverse immédiatement (cv2.flip) pour que l'affichage soit naturel pour toi (comme un miroir).

Le Viseur (ROI - Region of Interest) : Au lieu d'analyser toute l'image (ce qui est lourd), il dessine un cadre rouge au centre. Le programme ne "regarde" que ce qui se passe à l'intérieur de ce carré pour économiser de la puissance de calcul.

Calcul de la "Signature" (ORB) : À l'intérieur de ce cadre, l'algorithme cherche des points stratégiques (coins, contrastes, formes). Il transforme ces points en une liste de nombres (les descripteurs).

Le Match (La comparaison) : Il compare les nombres du viseur avec ceux de ton image de référence. Il utilise la distance de Hamming pour voir si les "signatures" se ressemblent.

Le Verdict : * Il compte le nombre de points communs (matches).

Si > 400 : L'objet est reconnu ! Le cadre devient Vert et il affiche "OBJET DÉTECTÉ".

Sinon : Il reste en Rouge et continue de chercher."""
