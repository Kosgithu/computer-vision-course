#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5.2 - Détection de Voitures dans une Vidéo
Détection de voitures en temps réel dans un flux vidéo

Source prof : /home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Image_processing_projects/Project_2-Detecting_Cars_in_Video
"""

import cv2
import time


def detection_voitures_video():
    """
    Détection de voitures dans une vidéo préenregistrée.
    Utilise un classificateur Haar Cascade spécifique aux voitures.
    """
    # ═══════════════════════════════════════════════════════════════
    # CHARGEMENT DU CLASSIFICATEUR
    # ═══════════════════════════════════════════════════════════════
    
    # Charge le fichier cascade pour la détection de voitures
    # Ce fichier XML contient les caractéristiques apprises pour reconnaître les voitures
    cars_detect = cv2.CascadeClassifier('haarcascade_car.xml')
    
    # Vérifier que le classificateur est bien chargé
    if cars_detect.empty():
        raise IOError("Impossible de charger haarcascade_car.xml")
    
    print("✅ Classificateur chargé")
    
    # ═══════════════════════════════════════════════════════════════
    # OUVERTURE DE LA VIDÉO
    # ═══════════════════════════════════════════════════════════════
    
    # Ouverture du fichier vidéo
    # 'cars.avi' = fichier vidéo préenregistré
    # Vous pouvez aussi utiliser 0 pour la webcam : cv2.VideoCapture(0)
    capture = cv2.VideoCapture('cars.avi')
    
    # Vérifier que la vidéo a été ouverte
    if not capture.isOpened():
        raise IOError("Impossible d'ouvrir la vidéo cars.avi")
    
    print("✅ Vidéo ouverte")
    print("🚗 Démarrage de la détection...")
    print("   Appuyez sur ESC pour quitter")
    
    # ═══════════════════════════════════════════════════════════════
    # BOUCLE PRINCIPALE
    # ═══════════════════════════════════════════════════════════════
    
    frame_count = 0
    
    # Tant que la vidéo est ouverte
    while capture.isOpened():
        # Pause pour ralentir la lecture
        # Sans cela, la vidéo défile trop vite sur les machines rapides
        time.sleep(0.05)  # 50ms = ~20 FPS
        
        # Lecture d'une frame
        # ret = True si la frame est lue correctement
        # frame = l'image capturée (numpy array)
        ret, frame = capture.read()
        
        # Vérifier que la lecture a réussi
        if not ret:
            print("Fin de la vidéo")
            break
        
        frame_count += 1
        
        # ═══════════════════════════════════════════════════════════
        # PRÉ-TRAITEMENT
        # ═══════════════════════════════════════════════════════════
        
        # Conversion en niveaux de gris (requis pour Haar Cascade)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # ═══════════════════════════════════════════════════════════
        # DÉTECTION DES VOITURES
        # ═══════════════════════════════════════════════════════════
        
        # Détecte les objets (voitures) de différentes tailles
        #
        # detectMultiScale(image, scaleFactor, minNeighbors)
        #
        #   scaleFactor (1.4) : Facteur de réduction entre chaque scan
        #       → 1.4 = réduit de 40% entre chaque passe
        #       → Plus élevé que pour les visages (1.3) car les voitures
        #         ont des tailles très variables
        #
        #   minNeighbors (2) : Nombre minimum de rectangles voisins pour valider
        #       → Plus permissif que pour les visages (5)
        #       → Car les voitures peuvent être partiellement cachées
        #
        cars = cars_detect.detectMultiScale(gray, 1.4, 2)
        
        # ═══════════════════════════════════════════════════════════
        # AFFICHAGE DES DÉTECTIONS
        # ═══════════════════════════════════════════════════════════
        
        # Dessiner un rectangle bleu autour de chaque voiture détectée
        for (x, y, w, h) in cars:
            # (x, y) = coin supérieur gauche
            # (x+w, y+h) = coin inférieur droit
            # (255, 0, 0) = couleur bleue en BGR
            # 3 = épaisseur du trait en pixels
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
            
            # Optionnel : ajouter un label
            # cv2.putText(frame, 'Voiture', (x, y-10),
            #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Afficher le nombre de voitures détectées
        if len(cars) > 0:
            cv2.putText(frame, f'Voitures: {len(cars)}', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Afficher le numéro de frame
        cv2.putText(frame, f'Frame: {frame_count}', (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # ═══════════════════════════════════════════════════════════
        # AFFICHAGE
        # ═══════════════════════════════════════════════════════════
        
        cv2.imshow('Voitures détectées', frame)
        
        # Sortie si touche ESC (code 27) pressée
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            print("Arrêt demandé")
            break
    
    # ═══════════════════════════════════════════════════════════════
    # NETTOYAGE
    # ═══════════════════════════════════════════════════════════════
    
    # Libération de la vidéo
    capture.release()
    
    # Fermeture de toutes les fenêtres
    cv2.destroyAllWindows()
    
    print("═══════════════════════════════════════")
    print(f"📊 Total frames traitées : {frame_count}")
    print("═══════════════════════════════════════")
    print("✅ Détection terminée")


if __name__ == "__main__":
    detection_voitures_video()
