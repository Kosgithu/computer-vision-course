# Thresholding (Seuillage) - Binarisation d'images
# Le seuillage convertit une image en niveaux de gris en image binaire (noir et blanc)
#
# Principe : Chaque pixel est comparé à un seuil. S'il est au-dessus = blanc, sinon = noir.

# Importation du package Computer Vision - cv2
import cv2

# Importation du package Python Numérique - numpy
# numpy est utilisé pour la manipulation des tableaux (les images sont des arrays)
import numpy as np

# ============================================================
# ÉTAPE 1 : Charger l'image originale
# ============================================================

# Lire l'image avec la fonction intégrée imread
# L'image doit être dans le même dossier que ce script
image = cv2.imread('image_6.jpg')

# Vérifier que l'image a bien été chargée
if image is None:
    print("Erreur : Impossible de charger l'image. Vérifiez le chemin.")
    exit()

# Afficher l'image originale avec la fonction intégrée imshow
cv2.imshow("Original", image)

# Attendre qu'une touche soit pressée avant de continuer
cv2.waitKey(0)

# ============================================================
# ÉTAPE 2 : Conversion en niveaux de gris
# ============================================================
#
# Pourquoi convertir en gris avant le seuillage ?
# Le seuillage s'applique sur UNE SEULE valeur par pixel (intensité 0-255)
# Une image couleur a 3 valeurs (B, G, R), donc on la simplifie d'abord en gris
#
# cv2.COLOR_BGR2GRAY : Code de conversion d'espace colorimétrique
# - BGR = Blue, Green, Red (OpenCV utilise cet ordre, pas RGB !)
# - Les bytes sont inversés par rapport au standard RGB
# - GRAY = Niveaux de gris (1 seul canal, 0=noir, 255=blanc)
#
# cv2.cvtColor() : Fonction de conversion entre espaces colorimétriques
# Très polyvalente : BGR↔RGB, BGR↔GRAY, BGR↔HSV, etc.

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Afficher l'image en niveaux de gris
cv2.imshow("Niveaux de gris", gray)
cv2.waitKey(0)

# ============================================================
# ÉTAPE 3 : Seuillage binaire (Binary Thresholding)
# ============================================================
#
# Principe du seuillage :
# Pour chaque pixel, si sa valeur > seuil → pixel = valeur max (blanc)
#                           sinon      → pixel = 0 (noir)
#
# Syntaxe : cv2.threshold(src, thresh, maxval, type)
# - src      : Image source (doit être en niveaux de gris !)
# - thresh   : Valeur de seuil (0-255). Ici : 127 = milieu de la plage
# - maxval   : Valeur assignée si pixel > seuil. Ici : 255 (blanc)
# - type     : Type de seuillage. Ici : cv2.THRESH_BINARY
#
# Types de seuillage disponibles :
# - THRESH_BINARY     : pixel > thresh → maxval, sinon 0
# - THRESH_BINARY_INV : pixel > thresh → 0, sinon maxval (inversé)
# - THRESH_TRUNC      : pixel > thresh → thresh, sinon inchangé
# - THRESH_TOZERO     : pixel > thresh → inchangé, sinon 0
# - THRESH_TOZERO_INV : pixel > thresh → 0, sinon inchangé

ret, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
# Explication des valeurs :
# - 127 : seuil = milieu de la plage 0-255
# - 255 : valeur max = blanc pur
# - Résultat : pixels clairs (>127) → blanc, pixels foncés (<127) → noir
#
# ret contient la valeur du seuil utilisée (127 ici)
# threshold contient l'image binarisée (noir et blanc uniquement)

print(f"Valeur de seuil utilisée : {ret}")

# Afficher l'image binarisée
cv2.imshow('Binary Thresholding', threshold)

# Attendre qu'une touche soit pressée
cv2.waitKey(0)

# ============================================================
# VARIANTES DE SEUILLAGE (décommenter pour tester)
# ============================================================

# --- SEUILLAGE INVERSE ---
# Blanc devient noir, noir devient blanc
# ret2, thresh_inv = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow('Thresholding Inverse', thresh_inv)
# cv2.waitKey(0)

# --- TRUNCATION ---
# Pixels > seuil sont mis AU SEUIL (pas au max)
# Crée un effet "plafonné"
# ret3, thresh_trunc = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
# cv2.imshow('Truncation', thresh_trunc)
# cv2.waitKey(0)

# --- TO ZERO ---
# Pixels < seuil sont mis à 0, les autres inchangés
# Utile pour masquer les zones sombres
# ret4, thresh_tozero = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO)
# cv2.imshow('To Zero', thresh_tozero)
# cv2.waitKey(0)

# ============================================================
# RÉCAPITULATIF
# ============================================================
#
# Le seuillage binaire est UNE ÉTAPE FONDAMENTALE en Computer Vision :
#
# ✅ Avantages :
#   - Sépare l'objet d'intérêt du fond (foreground/background)
#   - Réduit la complexité (2 valeurs au lieu de 256)
#   - Préparation idéale pour la détection de contours
#
# ❌ Limites :
#   - Nécessite un bon choix de seuil (127 est arbitraire ici)
#   - Marche mal avec éclairage variable
#   - Un seul seuil pour toute l'image → solution : seuillage adaptatif
#
# 🔧 Applications concrètes :
#   - Détection de documents (scanner)
#   - Segmentation d'objets sur fond uni
#   - Pré-traitement OCR (reconnaissance de texte)
#   - Détection de formes simples

# Fermer toutes les fenêtres ouvertes par cv2.imshow()
cv2.destroyAllWindows()
