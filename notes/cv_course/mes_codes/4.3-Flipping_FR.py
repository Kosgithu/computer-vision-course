# Retournement d'Images - Horizontal, Vertical, Horizontal & Vertical

# Importation du package Computer Vision - cv2
import cv2

# Lire l'image avec la fonction intégrée imread
image = cv2.imread('image_3.jpg')

# Afficher l'image originale avec la fonction intégrée imshow
cv2.imshow("Original", image)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# cv2.flip sert à retourner les images
# Syntaxe : cv2.flip(image, flipCode)
# flipCode = 1  → retournement horizontal (miroir gauche-droite)
# flipCode = 0  → retournement vertical (haut-bas)
# flipCode = -1 → retournement horizontal ET vertical (rotation 180°)

# Retournement horizontal avec la valeur '1'
# C'est comme regarder dans un miroir : gauche et droite sont inversés
retournement = cv2.flip(image, 1)

# Afficher l'image retournée horizontalement
cv2.imshow("Retournement Horizontal", retournement)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Retournement vertical avec la valeur '0'
# L'image est retournée à l'envers : le haut devient le bas
retournement = cv2.flip(image, 0)

# Afficher l'image retournée verticalement
cv2.imshow("Retournement Vertical", retournement)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Retournement horizontal ET vertical avec la valeur '-1'
# Équivalent à une rotation de 180 degrés
retournement = cv2.flip(image, -1)

# Afficher l'image retournée horizontalement & verticalement
cv2.imshow("Retournement H & V", retournement)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Fermer toutes les fenêtres
cv2.destroyAllWindows()
