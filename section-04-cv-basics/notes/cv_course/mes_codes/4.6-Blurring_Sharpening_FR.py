# Flou (Blurring) et Netteté (Sharpening) d'Images
# Chapitre 4.6 - Computer Vision Course
# 
# Ce script montre :
# 1. Le flou par moyenne (Averaging Blur)
# 2. Le renforcement de la netteté (Sharpening) avec un noyau personnalisé

# Importation du package Computer Vision - cv2
import cv2

# Importation du package Python Numérique - numpy
# numpy est utilisé pour créer et manipuler les noyaux (kernels) de convolution
import numpy as np

# ============================================================
# ÉTAPE 1 : Charger et afficher l'image originale
# ============================================================

# Lire l'image avec la fonction intégrée imread
# L'image doit être dans le même dossier que ce script, ou préciser le chemin complet
image = cv2.imread('image_5.jpg')

# Vérifier que l'image a bien été chargée
if image is None:
    print("Erreur : Impossible de charger l'image. Vérifiez le chemin.")
    exit()

# Afficher l'image originale avec la fonction intégrée imshow
cv2.imshow("Original", image)

# Attendre qu'une touche soit pressée avant de continuer
cv2.waitKey(0)

# ============================================================
# ÉTAPE 2 : Flou par moyenne (Averaging Blur)
# ============================================================
# 
# Principe : Chaque pixel est remplacé par la moyenne de ses voisins
# C'est une convolution avec un "filtre boîte normalisé" (normalized box filter)
#
# Qu'est-ce qu'une convolution ?
# C'est une opération mathématique qui combine deux fonctions pour en produire une troisième.
# En traitement d'image : on fait "glisser" un noyau (kernel) sur l'image et on calcule
# le produit scalaire à chaque position.
#
# Exemple de filtre boîte normalisé 3×3 :
# Chaque élément vaut 1/9, donc la somme = 1 (conservation de la luminosité)
# 
# (1/9) × | 1  1  1 |
#         | 1  1  1 |
#         | 1  1  1 |
#
# Syntaxe : cv2.blur(image, (taille_x, taille_y))
# - taille_x, taille_y : dimensions du noyau (doivent être des nombres positifs impairs)
# - Plus le noyau est grand, plus le flou est prononcé

blur = cv2.blur(image, (9, 9))
# Ici : noyau 9×9 → moyenne calculée sur 81 pixels voisins
# Cela crée un flou important, lisse les détails fins

# Afficher l'image floutée
cv2.imshow('Blurred (Flou Moyen 9x9)', blur)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# Note : Il existe d'autres types de flou non montrés dans ce fichier de base :
# - cv2.GaussianBlur() : flou pondéré, plus naturel
# - cv2.medianBlur() : remplace par la médiane, excellent contre le bruit "sel et poivre"
# - cv2.bilateralFilter() : flou qui préserve les bords

# ============================================================
# ÉTAPE 3 : Renforcement de la netteté (Sharpening)
# ============================================================
#
# Principe : Accentuer les contours et les détails de l'image
# On utilise une convolution avec un noyau spécifique qui met en valeur les différences
# entre un pixel et ses voisins (c'est-à-dire les bords)
#
# Le noyau de sharpening classique 3×3 utilisé ici :
#
# | -1  -1  -1 |
# | -1   9  -1 |
# | -1  -1  -1 |
#
# Explication :
# - Le centre (9) amplifie le pixel courant
# - Les -1 autour soustraient les pixels voisins
# - Résultat : les zones homogones restent stables (9-8=1)
#   mais les bords sont amplifiés (différence accentuée)
#
# IMPORTANT : La somme de tous les éléments du noyau doit égaler 1
# Si somme > 1 → image plus claire
# Si somme < 1 → image plus sombre
# Ici : (-1×8) + 9 = 1 ✓ (luminosité conservée)

kernel = np.array([[-1, -1, -1], 
                   [-1,  9, -1], 
                   [-1, -1, -1]], dtype=np.float32)
# dtype=np.float32 : important pour les calculs avec nombres négatifs

# Application du filtre avec cv2.filter2D
# Syntaxe : cv2.filter2D(image, ddepth, kernel)
# - image : image source
# - ddepth : profondeur de l'image de sortie
#   * -1 = même profondeur que l'image source (recommandé ici)
#   * cv2.CV_8U, cv2.CV_16S, cv2.CV_32F, cv2.CV_64F pour des profondeurs spécifiques
# - kernel : noyau de convolution (doit être un array numpy carré, impair)

sharpened = cv2.filter2D(image, -1, kernel)
# ddepth=-1 : l'image sharpened aura la même profondeur (8 bits par canal) que l'original

# Afficher l'image avec netteté renforcée
cv2.imshow('Sharpened (Netteté)', sharpened)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# ============================================================
# COMPARAISON VISUELLE
# ============================================================
# 
# Original   : Image de départ
# Blurred    : Détails lissés, contours adoucis
# Sharpened  : Contours accentués, peut apparaître "criard" si exagéré
#
# Astuce pratique : On peut combiner les deux !
# Par exemple : appliquer un léger flou pour réduire le bruit,
# puis un sharpening pour retrouver la netteté sur les contours importants.

# ============================================================
# EXEMPLE DE COMBINAISON (optionnel - décommenter pour tester)
# ============================================================
# # 1. D'abord un léger flou gaussien pour réduire le bruit
# denoised = cv2.GaussianBlur(image, (3, 3), 0)
# 
# # 2. Puis sharpening sur l'image débruitée
# sharpened_clean = cv2.filter2D(denoised, -1, kernel)
# 
# cv2.imshow('Denoised + Sharpened', sharpened_clean)
# cv2.waitKey(0)

# Fermer toutes les fenêtres ouvertes par cv2.imshow()
# Nécessaire pour libérer les ressources système
cv2.destroyAllWindows()
