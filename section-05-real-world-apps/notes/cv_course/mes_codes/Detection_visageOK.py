# -*- coding: utf-8 -*-
"""
Détection Temps Réel : Visage, Yeux et Nez
=========================================
Ce script utilise OpenCV avec Haar Cascades pour détecter les visages,
les yeux et le nez en temps réel avec la caméra du Raspberry Pi 5.

IMPORTANT - Pourquoi on utilise picamera2 au lieu de cv2.VideoCapture ?
---------------------------------------------------------------------------
Sur Raspberry Pi 5 avec caméra CSI, cv2.VideoCapture(0) ne fonctionne PAS
à cause d'un bug avec le backend GStreamer. La solution est d'utiliser
picamera2 pour capturer, puis OpenCV pour le traitement d'image.

Touches :
    ESC : Quitter le programme

Auteur : Madi
Date : 2026-03-04
"""

# =============================================================================
# IMPORTS
# =============================================================================
import cv2              # OpenCV : traitement d'image et computer vision
import numpy as np      # NumPy : manipulation de tableaux (images = tableaux)
import os               # OS : gestion des chemins de fichiers
import time             # Time : pauses et délais
from picamera2 import Picamera2  # Picamera2 : accès caméra Raspberry Pi 5

# =============================================================================
# CONFIGURATION DES CHEMINS
# =============================================================================
# On récupère le dossier où se trouve CE script, quel que soit l'endroit
# d'où on le lance. C'est important car sinon Python chercherait les fichiers
# XML dans le répertoire courant du terminal, pas dans le dossier du script.
script_dir = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# CHARGEMENT DES CLASSIFICATEURS HAAR CASCADE
# =============================================================================
# Les Haar Cascades sont des fichiers XML entraînés qui contiennent des
# modèles de détection. OpenCV les utilise pour repérer des patterns
# (visages, yeux, etc.) dans une image.
#
# PARAMÈTRES IMPORTANTS de detectMultiScale() :
#   scaleFactor (1.3) : Réduction de l'image à chaque étape. Plus c'est petit,
#                       plus la détection est précise mais lente.
#   minNeighbors (5)  : Nombre de rectangles voisins pour valider une détection.
#                       Plus c'est élevé, moins il y a de faux positifs.

print("📂 Chargement des classificateurs...")

face_detect = cv2.CascadeClassifier(
    os.path.join(script_dir, 'haarcascade_frontalface_alt.xml')
)
eyes_detect = cv2.CascadeClassifier(
    os.path.join(script_dir, 'haarcascade_eye.xml')
)
noise_detect = cv2.CascadeClassifier(
    os.path.join(script_dir, 'haarcascade_mcs_nose.xml')
)

# Vérification que les fichiers sont bien chargés
# Si .empty() renvoie True, le fichier XML n'a pas été trouvé ou est invalide
if face_detect.empty(): 
    raise IOError('❌ Impossible de charger haarcascade_frontalface_alt.xml')
if eyes_detect.empty():
    raise IOError('❌ Impossible de charger haarcascade_eye.xml')
if noise_detect.empty(): 
    raise IOError('❌ Impossible de charger haarcascade_mcs_nose.xml')

print("✅ Tous les classificateurs sont chargés")

# =============================================================================
# INITIALISATION DE LA CAMÉRA AVEC PICAMERA2
# =============================================================================
# Pourquoi pas cv2.VideoCapture(0) ?
# Sur Pi 5, VideoCapture utilise GStreamer qui a des bugs avec la caméra CSI.
# Picamera2 est la librairie officielle Raspberry Pi qui gère correctement :
# - L'initialisation du pipeline caméra
# - Le traitement d'image ISP (balance des blancs, exposition...)
# - L'encodage matériel

print("📹 Initialisation de la caméra (Picamera2)...")

picam2 = Picamera2()

# Configuration de la caméra
# "RGB888" = format BGR standard d'OpenCV (Blue, Green, Red sur 8 bits chacun)
# (640, 480) = résolution HD légère, suffisante pour la détection
config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)
picam2.configure(config)
picam2.start()

# Attendre que la caméra soit prête (exposition auto, balance des blancs...)
time.sleep(0.5)

print("🎬 Démarrage de la détection")
print("   Appuie sur ESC pour quitter\n")

# =============================================================================
# BOUCLE PRINCIPALE DE TRAITEMENT
# =============================================================================
# Cette boucle s'exécute indéfiniment jusqu'à ce qu'on appuie sur ESC

while True: 
    # -------------------------------------------------------------------------
    # 1. CAPTURE D'IMAGE
    # -------------------------------------------------------------------------
    # capture_array() récupère l'image sous forme de tableau NumPy
    # Format : [hauteur, largeur, 3 canaux] = [480, 640, 3] pour du BGR
    capturing = picam2.capture_array()
    
    # -------------------------------------------------------------------------
    # 2. PRÉ-TRAITEMENT
    # -------------------------------------------------------------------------
    # On réduit l'image de moitié (fx=0.5, fy=0.5) pour accélérer le traitement
    # La détection Haar fonctionne très bien sur des images réduites
    resize_frame = cv2.resize(
        capturing, 
        None, 
        fx=0.5, 
        fy=0.5, 
        interpolation=cv2.INTER_AREA  # Interpolation de bonne qualité pour réduction
    )
    
    # Conversion en niveaux de gris
    # Pourquoi ? La détection Haar fonctionne sur 1 canal (gris), pas 3 (couleur)
    # C'est aussi plus rapide et moins sensible aux variations de lumière
    gray = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)
    
    # -------------------------------------------------------------------------
    # 3. DÉTECTION DES VISAGES
    # -------------------------------------------------------------------------
    # detectMultiScale analyse l'image et renvoie une liste de rectangles
    # Chaque rectangle = [x, y, largeur, hauteur] d'un visage détecté
    face_detection = face_detect.detectMultiScale(
        gray,           # Image en niveaux de gris
        scaleFactor=1.3,  # Réduction de 30% à chaque passe
        minNeighbors=5    # Au moins 5 détections proches pour valider
    )
    
    # -------------------------------------------------------------------------
    # 4. TRAITEMENT DE CHAQUE VISAGE DÉTECTÉ
    # -------------------------------------------------------------------------
    # On boucle sur tous les visages trouvés (souvent 0 ou 1, parfois plusieurs)
    for (x, y, w, h) in face_detection: 
        
        # --- Dessiner un rectangle rouge autour du visage ---
        # cv2.rectangle(image, coin_haut_gauche, coin_bas_droit, couleur, épaisseur)
        # Couleur BGR : (0, 0, 255) = Rouge pur
        cv2.rectangle(resize_frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        
        # --- Extraction de la ROI (Region Of Interest) ---
        # On isole la zone du visage pour chercher yeux et nez DANS le visage
        # Ça évite de détecter des yeux ailleurs dans l'image
        gray_roi = gray[y:y+h, x:x+w]      # ROI en niveaux de gris (pour la détection)
        color_roi = resize_frame[y:y+h, x:x+w]  # ROI en couleur (pour le dessin)
        
        # --- DÉTECTION DES YEUX (dans la ROI du visage) ---
        eye_detector = eyes_detect.detectMultiScale(gray_roi)
        for (eye_x, eye_y, eye_w, eye_h) in eye_detector:
            # Rectangle bleu autour des yeux (255, 0, 0) = Bleu BGR
            cv2.rectangle(
                color_roi, 
                (eye_x, eye_y), 
                (eye_x + eye_w, eye_y + eye_h), 
                (255, 0, 0), 
                2
            )
        
        # --- DÉTECTION DU NEZ (dans la ROI du visage) ---
        noise_detector = noise_detect.detectMultiScale(
            gray_roi, 
            scaleFactor=1.3, 
            minNeighbors=5
        )
        for (nose_x, nose_y, nose_w, nose_h) in noise_detector:
            # Rectangle vert autour du nez (0, 255, 0) = Vert BGR
            cv2.rectangle(
                color_roi, 
                (nose_x, nose_y), 
                (nose_x + nose_w, nose_y + nose_h), 
                (0, 255, 0), 
                2
            )
            
    # -------------------------------------------------------------------------
    # 5. AFFICHAGE
    # -------------------------------------------------------------------------
    # On affiche l'image avec les rectangles dessinés
    # La fenêtre se met à jour à chaque itération (~30-60 fps selon le Pi)
    cv2.imshow("Detection Temps Reel - Visage(Rouge) Yeux(Bleu) Nez(Vert)", resize_frame)
    
    # -------------------------------------------------------------------------
    # 6. GESTION DES ÉVÉNEMENTS CLAVIER
    # -------------------------------------------------------------------------
    # waitKey(1) attend 1ms et récupère la touche pressée
    # 27 = code ASCII de la touche ESC (Échap)
    c = cv2.waitKey(1)
    if c == 27:
        print("\n👋 Fermeture demandée (ESC)")
        break

# =============================================================================
# NETTOYAGE ET FERMETURE
# =============================================================================
# IMPORTANT : Toujours libérer les ressources pour éviter :
# - La caméra reste occupée (impossible de la réutiliser)
# - Les fuites mémoire
# - Les fenêtres zombies

print("🧹 Libération des ressources...")
picam2.stop()           # Arrête la caméra proprement
cv2.destroyAllWindows()  # Ferme toutes les fenêtres OpenCV

print("✅ Programme terminé")

# =============================================================================
# ASTUCES ET DÉPANNAGE
# =============================================================================
# 
# 1. La détection est lente ?
#    → Réduis plus l'image : fx=0.3, fy=0.3
#    → Augmente scaleFactor : 1.5 au lieu de 1.3
#
# 2. Trop de faux positifs (détecte des visages qui n'existent pas) ?
#    → Augmente minNeighbors : 10 au lieu de 5
#    → Utilise haarcascade_frontalface_default.xml (plus strict)
#
# 3. La détection manque des visages ?
#    → Diminue scaleFactor : 1.1 (mais plus lent)
#    → Diminue minNeighbors : 3 (mais plus de faux positifs)
#
# 4. Les yeux/nez ne sont pas détectés ?
#    → Vérifie que les fichiers XML sont bien dans le dossier
#    → Assure-toi que le visage est bien détecté d'abord
#    → Éclaire mieux le sujet (évite les ombres sur le visage)
#
# 5. Erreur "cannot open camera" ?
#    → Vérifie que la caméra CSI est bien branchée
#    → Vérifie qu'elle est activée avec : sudo raspi-config
#    → Redémarre le Pi après activation de la caméra
#
# =============================================================================
