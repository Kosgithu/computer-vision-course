# Érosion et Dilatation - Opérations Morphologiques
# Érosion : Supprime les pixels aux frontières des objets (rétrécit)
# Dilatation : Ajoute des pixels aux frontières des objets (grossit)

# Importation du package Computer Vision - cv2
import cv2

# Importation du package Numerical Python - numpy sous l'alias np
import numpy as np

# Lecture de l'image avec la fonction intégrée imread
image = cv2.imread('image_7.jpg')

# Affichage de l'image originale avec la fonction intégrée imshow
cv2.imshow("Originale", image)

# Attente jusqu'à ce qu'une touche soit pressée
cv2.waitKey(0)

# np.ones retourne un tableau rempli de 1, selon la forme et le type donnés
# np.ones(forme, dtype)
kernel = np.ones((5, 5), dtype="uint8")
# 5 x 5 sont les dimensions du kernel (noyau)
# uint8 : entier non signé (0 à 255), standard pour les images

# cv2.erode est la fonction intégrée pour l'érosion
# cv2.erode(image, kernel, iterations)
erosion = cv2.erode(image, kernel, iterations=1)
# iterations=1 : nombre de passes de l'opération

# Affichage de l'image après érosion
cv2.imshow("Erosion", erosion)

# Attente jusqu'à ce qu'une touche soit pressée
cv2.waitKey(0)

# cv2.dilate est la fonction intégrée pour la dilatation
# cv2.dilate(image, kernel, iterations)
dilation = cv2.dilate(image, kernel, iterations=1)

# Affichage de l'image après dilatation
cv2.imshow("Dilatation", dilation)

# Attente jusqu'à ce qu'une touche soit pressée
cv2.waitKey(0)

# Fermeture de toutes les fenêtres
cv2.destroyAllWindows()

# =============================================================================
# EXPLICATIONS COMPLÉMENTAIRES
# =============================================================================

# --- LE KERNEL (NOYAU) ---
# C'est une petite matrice qui définit la "zone d'action" de l'opération.
# Imagine une gomme carrée (pour l'érosion) ou un crayon épais (pour la dilatation).
# Plus le kernel est grand, plus l'effet est prononcé.
#
# Autres tailles possibles :
# kernel = np.ones((3, 3), dtype="uint8")  # Effet léger et précis
# kernel = np.ones((7, 7), dtype="uint8")  # Effet fort et grossier

# --- LES ITÉRATIONS ---
# Définissent combien de fois on applique l'opération.
# C'est comme passer plusieurs coups de gomme au même endroit.
#
# iterations=1 : Un seul passage (effet léger)
# iterations=3 : Trois passages (effet modéré)
# iterations=5 : Cinq passages (effet fort)

# --- OPENING ET CLOSING (Combinaisons puissantes) ---
# Opening (Ouverture) = Érosion puis Dilatation
# → Supprime le bruit (petits points blancs isolés)
# opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
#
# Closing (Fermeture) = Dilatation puis Érosion
# → Comble les trous dans les objets
# closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# =============================================================================
# ASTUCES / PIÈGES
# =============================================================================
# ⚠️ L'ordre des opérations compte ! Érosion + Dilatation ≠ Dilatation + Érosion
# ⚠️ Ces opérations modifient la taille des objets dans l'image !
# ⚠️ Sur images couleur : applique sur un canal ou convertis en niveaux de gris
#
# ✅ Pour nettoyer le bruit : utilise Opening (érosion → dilatation)
# ✅ Pour combler les trous : utilise Closing (dilatation → érosion)
# ✅ Commence avec iterations=1, augmente progressivement si besoin
# ✅ Kernel 3×3 ou 5×5 suffisent dans 90% des cas
