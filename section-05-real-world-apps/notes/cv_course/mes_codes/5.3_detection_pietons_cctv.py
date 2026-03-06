#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5.3 - Détection de Piétons (CCTV)
Détection de piétons en temps réel avec caméra de surveillance

Source prof : /home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Image_processing_projects/Project_3-People_Detection_CCTV
"""

import cv2
import time


def detection_pietons_cctv():
    """
    Détection de piétons en temps réel avec caméra CCTV.
    Utilise deux classificateurs : fullbody et upperbody.
    """
    # ═══════════════════════════════════════════════════════════════
    # CHARGEMENT DES CLASSIFICATEURS
    # ═══════════════════════════════════════════════════════════════
    
    # Charge le classificateur pour détecter le corps entier
    body_detect = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    
    # Charge le classificateur pour détecter le haut du corps (tête + torse)
    upperbody_detect = cv2.CascadeClassifier('haarcascade_upperbody.xml')
    
    # Vérifier que les classificateurs sont bien chargés
    if body_detect.empty():
        raise IOError("Impossible de charger haarcascade_fullbody.xml")
    if upperbody_detect.empty():
        raise IOError("Impossible de charger haarcascade_upperbody.xml")
    
    print("✅ Classificateurs chargés")
    
    # ═══════════════════════════════════════════════════════════════
    # OUVERTURE DE LA SOURCE VIDÉO
    # ═══════════════════════════════════════════════════════════════
    
    # Ouverture de la caméra par défaut (0)
    # Vous pouvez aussi utiliser un fichier vidéo : cv2.VideoCapture('cctv.mp4')
    capture = cv2.VideoCapture(0)
    
    if not capture.isOpened():
        raise IOError("Impossible d'ouvrir la caméra")
    
    print("✅ Caméra ouverte")
    print("🚶 Démarrage de la détection...")
    print("   Appuyez sur ESC pour quitter")
    
    # ═══════════════════════════════════════════════════════════════
    # BOUCLE PRINCIPALE
    # ═══════════════════════════════════════════════════════════════
    
    frame_count = 0
    person_count = 0
    
    while capture.isOpened():
        # Lecture d'une frame
        ret, frame = capture.read()
        
        if not ret:
            print("Erreur de lecture")
            break
        
        frame_count += 1
        
        # ═══════════════════════════════════════════════════════════
        # PRÉ-TRAITEMENT
        # ═══════════════════════════════════════════════════════════
        
        # Conversion en niveaux de gris (requis pour Haar Cascade)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # ═══════════════════════════════════════════════════════════
        # DÉTECTION DES PIÉTONS
        # ═══════════════════════════════════════════════════════════
        
        # Détection corps entier
        # scaleFactor=1.1 : scan fin pour différentes tailles
        # minNeighbors=3 : équilibré entre précision et faux positifs
        bodies = body_detect.detectMultiScale(gray, 1.1, 3)
        
        # Détection haut du corps
        upper_bodies = upperbody_detect.detectMultiScale(gray, 1.1, 3)
        
        # ═══════════════════════════════════════════════════════════
        # AFFICHAGE DES DÉTECTIONS
        # ═══════════════════════════════════════════════════════════
        
        # Dessiner rectangles pour corps entier (vert)
        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, 'Personne', (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Dessiner rectangles pour haut du corps (bleu)
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
        
        # Afficher le compteur sur la frame
        cv2.putText(frame, f'Personnes: {person_count}', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Afficher le numéro de frame
        cv2.putText(frame, f'Frame: {frame_count}', (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # ═══════════════════════════════════════════════════════════
        # AFFICHAGE
        # ═══════════════════════════════════════════════════════════
        
        cv2.imshow('Detection Pietons CCTV', frame)
        
        # Sortie si ESC pressée
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            print("Arrêt demandé")
            break
    
    # ═══════════════════════════════════════════════════════════════
    # NETTOYAGE
    # ═══════════════════════════════════════════════════════════════
    
    capture.release()
    cv2.destroyAllWindows()
    
    print("═══════════════════════════════════════")
    print(f"📊 Total frames traitées : {frame_count}")
    print("═══════════════════════════════════════")
    print("✅ Détection terminée")


if __name__ == "__main__":
    detection_pietons_cctv()
