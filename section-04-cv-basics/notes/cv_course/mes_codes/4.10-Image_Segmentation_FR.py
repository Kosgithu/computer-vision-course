# Segmentation d'Image par Contours
# Segmentation : Partitionner l'image en différentes régions
# Contours : Lignes ou courbes autour de la limite d'un objet

# Import du package Computer Vision - cv2
import cv2

# Import du package Numerical Python - numpy sous l'alias np
import numpy as np

# Lecture de l'image avec la fonction intégrée imread
image = cv2.imread('image_9.jpg')

# Affichage de l'image originale
cv2.imshow("Original", image)
cv2.waitKey(0)

# ÉTAPE 1 : Détection des bords avec Canny
# cv2.Canny(image, seuil_min, seuil_max)
canny = cv2.Canny(image, 50, 200)

cv2.imshow("Detection Canny", canny)
cv2.waitKey(0)

# ÉTAPE 2 : Recherche des contours
# cv2.findContours(image_canny, mode_recuperation, mode_approximation)
# 
# Modes de récupération :
# - cv2.RETR_LIST : récupère tous les contours (pas de hiérarchie)
# - cv2.RETR_EXTERNAL : récupère uniquement les contours extérieurs
# - cv2.RETR_TREE : récupère tous avec hiérarchie complète
#
# Méthodes d'approximation :
# - cv2.CHAIN_APPROX_NONE : stocke TOUS les points du contour
# - cv2.CHAIN_APPROX_SIMPLE : stocke uniquement les points essentiels

contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

print(f"Nombre de contours trouvés : {len(contours)}")

# ÉTAPE 3 : Dessiner les contours sur l'image
# cv2.drawContours(image, contours, index_contour, couleur, epaisseur)
# - index_contour = -1 dessine TOUS les contours
# - couleur au format BGR : (255,0,0) = Bleu, (0,255,0) = Vert, (0,0,255) = Rouge
# - epaisseur en pixels

cv2.drawContours(image, contours, -1, (255, 0, 0), 10)

# Affichage des contours
cv2.imshow("Contours", image)
cv2.waitKey(0)

# Fermeture de toutes les fenêtres
cv2.destroyAllWindows()

# BONUS : Analyser les contours trouvés
# for i, contour in enumerate(contours):
#     aire = cv2.contourArea(contour)  # Surface en pixels²
#     perimetre = cv2.arcLength(contour, True)  # Longueur du contour (True = fermé)
#     print(f"Contour {i}: aire = {aire:.0f}, périmètre = {perimetre:.0f}")
