# -*- coding: utf-8 -*-
"""
Détection de Voitures dans une Vidéo
====================================
Ce script détecte les voitures dans une vidéo en utilisant un Haar Cascade
spécifiquement entraîné pour reconnaître les véhicules.

Paramètres optimisés pour voitures :
- scaleFactor = 1.4 (les voitures ont des tailles très variables)
- minNeighbors = 2 (plus permissif car voitures partiellement cachées)

Touches :
    ESC : Quitter le programme

Auteur : Madi (traduction et commentaires FR)
Date : 2026-03-04
Source : Cours Udemy Computer Vision
"""

import cv2
import time

# =============================================================================
# CHARGEMENT DU CLASSIFICATEUR POUR VOITURES
# =============================================================================
# Le fichier haarcascade_car.xml contient des milliers d'exemples de voitures
# entraînés pour reconnaître différents angles et types de véhicules
print("📂 Chargement du classificateur de voitures...")

cars_detect = cv2.CascadeClassifier('haarcascade_car.xml')

# Vérification du chargement
if cars_detect.empty():
    raise IOError("""
    ❌ Impossible de charger haarcascade_car.xml
    
    Téléchargez le fichier avec :
    wget https://raw.githubusercontent.com/andrewssobral/vehicle_detection_haarcascades/master/haarcascade_car.xml
    """)

print("✅ Classificateur chargé avec succès")

# =============================================================================
# OUVERTURE DE LA VIDÉO
# =============================================================================
# VideoCapture peut ouvrir :
# - Un fichier vidéo : cv2.VideoCapture('fichier.avi')
# - Une caméra : cv2.VideoCapture(0)
#
# Formats supportés : .avi (MJPEG), .mp4 (avec codecs)

print("🎬 Ouverture de la vidéo...")
capture = cv2.VideoCapture('cars.avi')

# Vérification que la vidéo s'est ouverte
if not capture.isOpened():
    raise IOError("""
    ❌ Impossible d'ouvrir cars.avi
    
    Vérifiez que :
    1. Le fichier existe dans le dossier courant
    2. Le format est supporté (.avi recommandé)
    3. Les codecs vidéo sont installés
    
    Pour convertir une vidéo :
    ffmpeg -i video.mp4 -c:v mjpeg -q:v 3 cars.avi
    """)

print("✅ Vidéo ouverte avec succès")
print("💡 Appuyez sur ESC pour quitter\n")

# =============================================================================
# BOUCLE DE LECTURE ET DÉTECTION
# =============================================================================
# On lit la vidéo frame par frame jusqu'à la fin ou interruption

frame_count = 0

while capture.isOpened():
    # -------------------------------------------------------------------------
    # CONTRÔLE DE VITESSE
    # -------------------------------------------------------------------------
    # time.sleep() est ESSENTIEL ici ! Sans ça, la vidéo défile trop vite
    # sur les machines rapides (une vidéo de 10s peut se lire en 2s)
    #
    # Valeurs recommandées :
    #   0.1  = lent (10 fps) - pour analyser en détail
    #   0.05 = normal (20 fps) - vitesse confortable
    #   0.01 = rapide (100 fps) - pour traitement rapide
    
    time.sleep(0.05)  # 50ms de pause = ~20 fps
    
    # -------------------------------------------------------------------------
    # LECTURE D'UNE FRAME
    # -------------------------------------------------------------------------
    # capture.read() retourne :
    #   ret   : True si la lecture a réussi, False si fin de vidéo ou erreur
    #   frame : L'image lue (tableau numpy)
    
    ret, frame = capture.read()
    
    # Sécurité : arrêter si plus de frames (fin de vidéo)
    if not ret:
        print("\n🏁 Fin de la vidéo atteinte")
        break
    
    frame_count += 1
    
    # -------------------------------------------------------------------------
    # PRÉ-TRAITEMENT
    # -------------------------------------------------------------------------
    # Conversion en niveaux de gris pour la détection Haar Cascade
    # (même principe que pour les visages)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # -------------------------------------------------------------------------
    # DÉTECTION DES VOITURES
    # -------------------------------------------------------------------------
    # PARAMÈTRES SPÉCIFIQUES AUX VOITURES :
    #
    # scaleFactor = 1.4
    #   - Plus élevé que pour les visages (1.3)
    #   - Car les voitures ont des tailles TRÈS variables
    #     (proche vs lointain, SUV vs compact...)
    #
    # minNeighbors = 2
    #   - Plus permissif que pour les visages (5)
    #   - Accepte des détections partielles (voitures cachées, angle de vue)
    
    cars_detected = cars_detect.detectMultiScale(
        gray,           # Image en niveaux de gris
        scaleFactor=1.4,  # Pas de réduction de 40% à chaque itération
        minNeighbors=2    # Minimum 2 rectangles voisins pour valider
    )
    
    # -------------------------------------------------------------------------
    # DESSIN DES RECTANGLES
    # -------------------------------------------------------------------------
    # Pour chaque voiture détectée, on dessine un rectangle bleu
    # Couleur BGR : (255, 0, 0) = Bleu pur
    
    for (x, y, w, h) in cars_detected:
        cv2.rectangle(
            frame,              # Image sur laquelle dessiner
            (x, y),             # Coin supérieur gauche
            (x + w, y + h),     # Coin inférieur droit
            (255, 0, 0),        # Couleur BLEUE (BGR)
            3                   # Épaisseur du trait
        )
    
    # -------------------------------------------------------------------------
    # AFFICHAGE
    # -------------------------------------------------------------------------
    cv2.imshow('Détection de Voitures', frame)
    
    # Afficher la progression toutes les 30 frames (~1.5s à 20fps)
    if frame_count % 30 == 0:
        print(f"🎞️  Frames traitées : {frame_count}", end='\r')
    
    # -------------------------------------------------------------------------
    # GESTION CLAVIER
    # -------------------------------------------------------------------------
    # waitKey(1) attend 1ms et récupère la touche pressée
    # 27 = code ASCII de la touche ESC
    
    c = cv2.waitKey(1)
    if c == 27:
        print("\n\n👋 Interruption par l'utilisateur (ESC)")
        break

# =============================================================================
# NETTOYAGE
# =============================================================================
print(f"\n📊 Total de frames traitées : {frame_count}")
print("🧹 Libération des ressources...")

capture.release()        # Ferme le fichier vidéo/libère la caméra
cv2.destroyAllWindows()  # Ferme toutes les fenêtres OpenCV

print("✅ Programme terminé")

# =============================================================================
# ASTUCES ET VARIANTES
# =============================================================================
#
# 1. AMÉLIORER LA PRÉCISION :
#    cars = cars_detect.detectMultiScale(gray, 1.2, 5)
#    - scaleFactor 1.2 = plus de détections mais plus lent
#    - minNeighbors 5 = moins de faux positifs
#
# 2. DÉTECTION SUR CAMÉRA EN DIRECT :
#    capture = cv2.VideoCapture(0)  # Au lieu du fichier
#    # Supprimer time.sleep() pour du temps réel
#
# 3. SAUVEGARDER LA VIDÉO AVEC LES DÉTECTIONS :
#    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))
#    out.write(frame)  # Dans la boucle
#
# 4. AJOUTER UN COMPTEUR DE VOITURES :
#    total_cars = len(cars_detected)
#    cv2.putText(frame, f'Voitures: {total_cars}', (10, 30),
#                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#
# 5. FILTRER LES PETITES DÉTECTIONS (bruit) :
#    for (x, y, w, h) in cars_detected:
#        if w > 50 and h > 50:  # Ignorer les objets trop petits
#            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
#
# =============================================================================
