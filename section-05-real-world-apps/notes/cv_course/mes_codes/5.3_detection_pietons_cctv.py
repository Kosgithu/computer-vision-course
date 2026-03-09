#!/usr/bin/env python3
# -*- coding: utf-8 -*-



# Importation du package Computer Vision - cv2
import cv2

# Importation du package Numerical Python - numpy
import numpy as np

# Importation du package Time pour la fonction sleep()
import time

# Chargement du fichier cascade pour les piétons via cv2.CascadeClassifier
# cv2.CascadeClassifier([nom_du_fichier]) 
pedestrian_detect = cv2.CascadeClassifier('haarcascade_fullbody.xml')

# Initialisation de l'objet de capture vidéo pour un fichier vidéo 
capture = cv2.VideoCapture('walking.avi')

# Initialisation de la boucle While jusqu'à ce que la touche Echap soit pressée
# VideoCapture.isOpened renvoie True si la vidéo est ouverte avec succès
while capture.isOpened():
    
    # Pause du programme (en secondes) pour réguler la vitesse de lecture
    time.sleep(.05)

    # Début de la capture des images (frames)
    ret, frame = capture.read()
    
    # Vérification si l'image a bien été reçue (évite le crash à la fin de la vidéo)
    if not ret:
        break
    
    # Redimensionnement de l'image via cv2.resize
    # cv2.resize(image, taille_sortie, échelle_x, échelle_y, interpolation)
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

    # Conversion RGB vers Gris via cv2.COLOR_BGR2GRAY
    # BGR (les octets sont inversés dans OpenCV)
    # cv2.cvtColor : Convertit l'image d'un espace colorimétrique à un autre
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Détection de piétons de différentes tailles via detectMultiScale
    # scaleFactor : Spécifie la réduction de la taille de l'image à chaque étape
    # minNeighbors : Nombre de voisins qu'un rectangle doit avoir pour être conservé
    pedestrian_detected = pedestrian_detect.detectMultiScale(gray, 1.2, 3)
    
    # Extraction des boîtes de délimitation pour chaque corps identifié
    # Les rectangles sont dessinés via la fonction cv2.rectangle
    # cv2.rectangle(image, (x1,y1), (x2,y2), couleur, épaisseur)
    for (x, y, w, h) in pedestrian_detected:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
        
    # Affichage de l'image avec les détections (placé hors de la boucle for)
    cv2.imshow('Detection de Pietons', frame)

    # Vérifier si l'utilisateur a appuyé sur la touche Echap (Esc)
    c = cv2.waitKey(1)
    if c == 27:
        break

# Libérer le dispositif de capture
capture.release()

# Fermer toutes les fenêtres OpenCV
cv2.destroyAllWindows()
