# Redimensionnement d'Images - Interpolations Cubique, Area, Linéaire
# L'interpolation est une méthode d'estimation des valeurs entre des points de données connus

# Importation du package Computer Vision - cv2
import cv2

# Importation du package Python Numérique - numpy
# numpy est utilisé pour manipuler les tableaux multidimensionnels (les images sont des tableaux)
import numpy as np

# Lire l'image avec la fonction intégrée imread
image = cv2.imread('image_2.jpg')

# Afficher l'image originale avec la fonction intégrée imshow
cv2.imshow("Original", image)

# Attendre qu'une touche soit pressée
cv2.waitKey()

# Syntaxe de cv2.resize() :
# cv2.resize(image_source, taille_sortie, echelle_x, echelle_y, interpolation)
# On peut soit donner une taille absolue (width, height), soit des facteurs d'échelle (fx, fy)

# Redimensionnement avec interpolation cubique
# INTER_CUBIC : meilleure qualité pour agrandir, plus lent
# fx=0.75, fy=0.75 réduit l'image à 75% de sa taille originale
defin = cv2.resize(image, None, fx=.75, fy=.75, interpolation=cv2.INTER_CUBIC)

# Afficher l'image interpolée en cubique
cv2.imshow('Interpolation Cubique', defin)

# Attendre qu'une touche soit pressée
cv2.waitKey()

# Redimensionnement avec interpolation area
# INTER_AREA : idéal pour réduire, utilise la relation zone-pixel
# (600, 300) force une taille exacte de 600px de large sur 300px de haut
defin_skewed = cv2.resize(image, (600, 300), interpolation=cv2.INTER_AREA)

# Afficher l'image interpolée en area
cv2.imshow('Interpolation Area', defin_skewed)

# Attendre qu'une touche soit pressée
cv2.waitKey()

# Redimensionnement avec interpolation linéaire
# INTER_LINEAR : interpolation bilinéaire, bon compromis qualité/vitesse
# Valeur par défaut si non spécifié, fx=0.5 = réduction de moitié
defin_lineaire = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

# Afficher l'image interpolée en linéaire
cv2.imshow('Interpolation Linéaire', defin_lineaire)

# Attendre qu'une touche soit pressée
cv2.waitKey()

# Fermer toutes les fenêtres ouvertes par cv2.imshow()
# Nécessaire pour libérer les ressources système
cv2.destroyAllWindows()
