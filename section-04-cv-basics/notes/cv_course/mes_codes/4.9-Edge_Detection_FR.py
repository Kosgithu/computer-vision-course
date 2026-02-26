# Détection de Contours avec l'algorithme de Canny
# Les contours sont des ensembles de points (lignes) où la luminosité de l'image change brusquement

# Import du package Computer Vision - cv2
import cv2

# Import du package Numerical Python - numpy sous l'alias np
import numpy as np

# Lecture de l'image avec la fonction intégrée imread
image = cv2.imread('image_8.jpg')

# Affichage de l'image originale avec la fonction intégrée imshow
cv2.imshow("Original", image)

# Attente jusqu'à ce qu'une touche soit pressée
cv2.waitKey(0)

# cv2.Canny est la fonction intégrée pour détecter les contours
# cv2.Canny(image, seuil_1, seuil_2)
# - seuil_1 : seuil minimum (pixels en dessous = rejetés)
# - seuil_2 : seuil maximum (pixels au-dessus = contours forts)
# Les pixels entre les deux seuils sont conservés s'ils sont connectés à un contour fort

canny = cv2.Canny(image, 50, 200)

# Affichage de l'image avec contours détectés
cv2.imshow('Detection Canny', canny)

# Attente jusqu'à ce qu'une touche soit pressée
cv2.waitKey(0)

# Fermeture de toutes les fenêtres
cv2.destroyAllWindows()
