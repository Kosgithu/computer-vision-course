# 4.9 - Détection de Contours (Edge Detection)

## Concept
Identifier les **bords** d'une image — les zones où la luminosité change brutalement. C'est la base de l'analyse de formes et de la reconnaissance d'objets.

---

## Code minimal

```python
import cv2
import numpy as np

image = cv2.imread('image_8.jpg')

# Détection de contours avec Canny
canny = cv2.Canny(image, 50, 200)

cv2.imshow('Canny Edge Detection', canny)
cv2.waitKey(0)
```

---

## Algorithme de Canny

L'algorithme de **Canny** est la méthode la plus utilisée pour la détection de contours. Il fonctionne en 5 étapes :

1. **Réduction du bruit** (flou gaussien)
2. **Gradient** (détection des changements d'intensité)
3. **Suppression des non-maxima** (affinage des contours)
4. **Seuillage par hystérésis** (décision finale)

## Fonction détaillée

```python
cv2.Canny(image, threshold1, threshold2)
```

| Paramètre | Description | Valeurs typiques |
|-----------|-------------|------------------|
| `image` | Image source (niveaux de gris ou couleur) | - |
| `threshold1` | Seuil minimum | 50 - 100 |
| `threshold2` | Seuil maximum | 150 - 300 |

### Seuils d'hystérésis

```
Pixels avec gradient > threshold2  →  Contour FORT (conservé)
Pixels avec gradient < threshold1  →  Contour FAIBLE (rejeté)
Pixels entre les deux              →  Contour conservé SI connecté à un fort
```

**Règle empirique** : `threshold2 ≈ 2 × threshold1` ou `threshold2 ≈ 3 × threshold1`

| Seuils | Effet | Usage |
|--------|-------|-------|
| `50, 150` | Détecte beaucoup de contours | Images complexes |
| `100, 200` | Contours principaux seulement | Objets simples |
| `50, 300` | Très sensible | Détection fine |

---

## Analogie simple

Imagine que tu dessines au crayon sur une feuille de papier granuleuse :

- **Seuil bas** (50) : Tu remarques même les petites imperfections du papier → trop de détails
- **Seuil haut** (200) : Tu ne vois que les traits les plus foncés → contours principaux
- **Deux seuils** : Tu gardes les traits foncés, et les traits moyens SI ils touchent un trait foncé

---

## Cas d'usage projets

| Projet | Usage |
|--------|-------|
| **Reconnaissance de formes** | Identifier les contours avant classification |
| **Mesure d'objets** | Détecter les bords pour calculer dimensions |
| **Robot suiveur de ligne** | Détecter la ligne sur la route |
| **QR Code / Code-barres** | Isoler le code avant décodage |
| **Détection de visage** | Trouver les contours caractéristiques |

---

## Pièges / Astuces

⚠️ **Toujours réduire le bruit avant** Canny ! Utilise `cv2.GaussianBlur()` pour de meilleurs résultats :
```python
blurred = cv2.GaussianBlur(image, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)
```

⚠️ **Images couleur** : Canny fonctionne sur les canaux séparément, mais convertir en gris d'abord est souvent mieux :
```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
```

✅ **Tester différents seuils** : Commencer avec 50/150, ajuster selon le résultat

✅ **Contours épais ?** Réduire avec `cv2.erode()` avant Canny

---

## Avant / Après Canny

```
Image originale :        Après Canny (50, 200) :

███████████████            ░░░░░░░░░░░░░
██░░░░░░░░░░░██            ░░▓▓▓▓▓▓▓▓▓░░
██░█████████░██            ░░▓░░░░░░░▓░░
██░█░░░░░░░█░██    →       ░░▓░░▓▓▓░░▓░░
██░█░███░░░█░██            ░░▓░░▓░▓░░▓░░
██░█░░░░░░░█░██            ░░▓░░░░░░░▓░░
██░█████████░██            ░░▓▓▓▓▓▓▓▓▓░░
██░░░░░░░░░░░██            ░░░░░░░░░░░░░
███████████████
```

---

## Code complet commenté

```python
import cv2
import numpy as np

# Chargement de l'image
image = cv2.imread('image_8.jpg')

# Affichage original
cv2.imshow("Original", image)
cv2.waitKey(0)

# Détection de contours avec Canny
# threshold1=50 : seuil bas (pixels en dessous = rejetés)
# threshold2=200 : seuil haut (pixels au-dessus = contours forts)
canny = cv2.Canny(image, 50, 200)

# Affichage du résultat
cv2.imshow('Canny Edge Detection', canny)
cv2.waitKey(0)

cv2.destroyAllWindows()
```

---

## Prochaine étape

La détection de contours est souvent utilisée avec **findContours** pour extraire les formes (voir chapitre 4.10 - Segmentation).

---

## Code source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/4.9-Edge_Detection.py`
