# Variation de la Luminosité des Images avec Addition et Soustraction

# Importation du package Computer Vision - cv2
import cv2

# Importation du package Python Numérique - numpy
import numpy as np

# Lire l'image avec la fonction intégrée imread
image = cv2.imread('image_4.jpg')

# Afficher l'image originale avec la fonction intégrée imshow
cv2.imshow("Original", image)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# np.ones retourne un tableau de la forme donnée, rempli de 1
# Syntaxe : np.ones(forme, dtype)
# - forme : tuple (hauteur, largeur, canaux) → image.shape prend la forme de l'image originale
# - dtype : type de données → "uint8" = entier non signé (0 à 255), standard pour les images

matrice = np.ones(image.shape, dtype="uint8") * 120
# Explication ligne par ligne :
# - np.ones(image.shape) : crée un tableau de la même taille que l'image, rempli de 1
# - dtype="uint8" : chaque valeur est un entier 0-255 (1 octet non signé)
# - * 120 : multiplie chaque 1 par 120 → résultat : tableau rempli de 120 partout
# Cette matrice servira à augmenter ou diminuer la luminosité uniformément

# Ajouter la matrice à l'image originale augmente la luminosité
# Chaque pixel reçoit +120 (jusqu'à la saturation à 255 = blanc)
addition = cv2.add(image, matrice)
# cv2.add() est préférable à image + matrice car il gère la saturation :
# si un pixel est à 200 et on ajoute 120 : 200+120=320 → cv2.add() donne 255 (blanc)
# alors que numpy ferait un dépassement (overflow) avec un résultat incorrect

# Afficher l'image éclaircie
cv2.imshow("Addition (Plus Lumineux)", addition)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Soustraire la matrice de l'image originale diminue la luminosité
# Chaque pixel reçoit -120 (jusqu'à la saturation à 0 = noir)
soustraction = cv2.subtract(image, matrice)
# Même principe : cv2.subtract() gère la saturation à 0
# si un pixel est à 50 et on retire 120 : 50-120=-70 → cv2.subtract() donne 0 (noir)

# Afficher l'image assombrie
cv2.imshow("Soustraction (Plus Sombre)", soustraction)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Fermer toutes les fenêtres
cv2.destroyAllWindows()
