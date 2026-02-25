# Opérations Bitwise (Bit à Bit) - AND, OR, XOR, NOT

# Importation du package Computer Vision - cv2
import cv2

# Importation du package Python Numérique - numpy
import numpy as np

# np.zeros(shape, dtype) crée un tableau rempli de zéros
# Création d'un rectangle noir de 200x200 pixels (niveaux de gris)
rectangle = np.zeros((200, 200), np.uint8)
# (200, 200) = dimensions hauteur x largeur
# np.uint8 = entier non signé 8 bits (0-255), standard pour les images

# Création du rectangle avec la fonction cv2.rectangle
# Syntaxe : cv2.rectangle(image, (x1,y1), (x2,y2), couleur, épaisseur)
# - (20, 20) : coin supérieur gauche
# - (180, 180) : coin inférieur droit
# - 255 : couleur blanche (max pour uint8)
# - -1 : épaisseur = remplissage complet (plein)
cv2.rectangle(rectangle, (20, 20), (180, 180), 255, -1)

# Afficher le rectangle créé
cv2.imshow("Rectangle", rectangle)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Création d'un cercle noir de 200x200 pixels
cercle = np.zeros((200, 200), dtype="uint8")

# Création du cercle avec la fonction cv2.circle
# Syntaxe : cv2.circle(image, centre, rayon, couleur, épaisseur)
# - (100, 100) : centre du cercle (au milieu de l'image 200x200)
# - 100 : rayon en pixels
# - 255 : couleur blanche
# - -1 : remplissage complet
cv2.circle(cercle, (100, 100), 100, 255, -1)

# Afficher le cercle créé
cv2.imshow("Cercle", cercle)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Opération bitwise AND (ET) entre rectangle et cercle
# Syntaxe : cv2.bitwise_and(source1, source2)
# Résultat : pixel blanc (255) seulement si LES DEUX sources ont un pixel blanc
# → Garde uniquement l'intersection (zone commune)
Et = cv2.bitwise_and(rectangle, cercle)

# Table de vérité AND :
# A B | Sortie
# 0 0 | 0      (noir ET noir = noir)
# 0 1 | 0      (noir ET blanc = noir)
# 1 0 | 0      (blanc ET noir = noir)
# 1 1 | 1      (blanc ET blanc = blanc)

# Afficher le résultat de l'opération AND
cv2.imshow("AND (Intersection)", Et)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Opération bitwise OR (OU) entre rectangle et cercle
# Résultat : pixel blanc si AU MOINS UNE source a un pixel blanc
# → Garde l'union (tout ce qui est dans l'un OU l'autre)
Ou = cv2.bitwise_or(rectangle, cercle)

# Table de vérité OR :
# A B | Sortie
# 0 0 | 0
# 0 1 | 1
# 1 0 | 1
# 1 1 | 1

# Afficher le résultat de l'opération OR
cv2.imshow("OR (Union)", Ou)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Opération bitwise XOR (OU exclusif) entre rectangle et cercle
# Résultat : pixel blanc si UNE SEULE source a un pixel blanc (pas les deux)
# → Garde ce qui est différent entre les deux (union - intersection)
Xor = cv2.bitwise_xor(rectangle, cercle)

# Table de vérité XOR :
# A B | Sortie
# 0 0 | 0
# 0 1 | 1
# 1 0 | 1
# 1 1 | 0      ← différence avec OR : si les deux sont blancs → noir

# Afficher le résultat de l'opération XOR
cv2.imshow("XOR (Différence)", Xor)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Opération bitwise NOT (NON/inversion) sur le rectangle
# Résultat : inverse chaque pixel (noir → blanc, blanc → noir)
# Syntaxe : cv2.bitwise_not(source) - une seule source
Non_rect = cv2.bitwise_not(rectangle)

# Table de vérité NOT :
# A | Sortie
# 0 | 1
# 1 | 0

# Afficher le résultat du NOT sur le rectangle
cv2.imshow("NOT Rectangle (Inversé)", Non_rect)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Opération bitwise NOT sur le cercle
Non_cercle = cv2.bitwise_not(cercle)

# Afficher le résultat du NOT sur le cercle
cv2.imshow("NOT Cercle (Inversé)", Non_cercle)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Fermer toutes les fenêtres
cv2.destroyAllWindows()
