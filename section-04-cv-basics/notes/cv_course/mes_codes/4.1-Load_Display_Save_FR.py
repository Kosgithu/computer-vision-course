# Chargement, Affichage et Sauvegarde d'Images

# Importation du package Computer Vision - cv2
import cv2

# Lire l'image avec la fonction intégrée imread
# imread() charge une image depuis un fichier et la convertit en tableau numpy
# Paramètre : chemin vers l'image (relatif ou absolu)
image = cv2.imread('image_1.jpg')

# Afficher l'image originale avec la fonction intégrée imshow
# imshow() ouvre une fenêtre avec le titre spécifié
# Paramètres : titre de la fenêtre, image à afficher (tableau numpy)
cv2.imshow("Original", image)

# Attendre qu'une touche soit pressée
# waitKey(0) bloque l'exécution jusqu'à ce qu'une touche soit pressée
# Le paramètre est le délai en millisecondes (0 = infini)
cv2.waitKey(0)

# Sauvegarder l'image avec la fonction intégrée imwrite
# imwrite() enregistre l'image dans un fichier
# Paramètres : nom du fichier de sortie, image à sauvegarder
# Formats supportés : jpg, png, bmp, tiff...
cv2.imwrite("Saved Image.jpg", image)
