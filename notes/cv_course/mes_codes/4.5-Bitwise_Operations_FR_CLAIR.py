# Opérations Bitwise (Bit à Bit) - VERSION CLAIRE
# Les noms de variables sont explicites pour éviter la confusion

import cv2
import numpy as np

# ============================================================
# ÉTAPE 1 : Créer le canvas (toile) noire pour le rectangle
# ============================================================

# Création d'une image noire 200×200 pixels
# C'est notre "toile" sur laquelle on va dessiner
canvas_rectangle = np.zeros((200, 200), np.uint8)

# Dessiner un rectangle blanc sur le canvas
# Paramètres : image, coin supérieur gauche, coin inférieur droit, couleur, épaisseur (-1 = plein)
cv2.rectangle(canvas_rectangle, (20, 20), (180, 180), 255, -1)

# Afficher le résultat
cv2.imshow("Figure 1 : Rectangle", canvas_rectangle)
cv2.waitKey(0)

# ============================================================
# ÉTAPE 2 : Créer le canvas noir pour le cercle
# ============================================================

# Nouvelle toile noire pour le cercle
canvas_cercle = np.zeros((200, 200), dtype="uint8")

# Dessiner un cercle blanc au centre
# Paramètres : image, centre (x,y), rayon, couleur, épaisseur (-1 = plein)
cv2.circle(canvas_cercle, (100, 100), 100, 255, -1)

# Afficher le résultat
cv2.imshow("Figure 2 : Cercle", canvas_cercle)
cv2.waitKey(0)

# ============================================================
# ÉTAPE 3 : Opérations bitwise
# ============================================================

# --- OPÉRATION AND (ET) ---
# Résultat = zone commune aux deux figures (intersection)
resultat_and = cv2.bitwise_and(canvas_rectangle, canvas_cercle)
cv2.imshow("Operateur AND (Intersection)", resultat_and)
cv2.waitKey(0)

# --- OPÉRATION OR (OU) ---
# Résultat = union des deux figures (tout ce qui est dans l'un OU l'autre)
resultat_or = cv2.bitwise_or(canvas_rectangle, canvas_cercle)
cv2.imshow("Operateur OR (Union)", resultat_or)
cv2.waitKey(0)

# --- OPÉRATION XOR (OU exclusif) ---
# Résultat = zones différentes entre les deux figures
resultat_xor = cv2.bitwise_xor(canvas_rectangle, canvas_cercle)
cv2.imshow("Operateur XOR (Difference)", resultat_xor)
cv2.waitKey(0)

# --- OPÉRATION NOT (INVERSION) ---
# Résultat = inverse du rectangle (noir devient blanc, blanc devient noir)
resultat_not_rectangle = cv2.bitwise_not(canvas_rectangle)
cv2.imshow("Operateur NOT sur Rectangle (Negatif)", resultat_not_rectangle)
cv2.waitKey(0)

# Inversion du cercle
resultat_not_cercle = cv2.bitwise_not(canvas_cercle)
cv2.imshow("Operateur NOT sur Cercle (Negatif)", resultat_not_cercle)
cv2.waitKey(0)

# Fermer toutes les fenêtres
cv2.destroyAllWindows()
