# 4.10 - Segmentation par Contours

## Concept
La **segmentation** divise l'image en régions distinctes. Les **contours** sont des lignes fermées qui délimitent ces régions (les objets).

Différence clé :
- **Edge Detection (4.9)** : Trouve les bords (lignes)
- **Segmentation** : Identifie les formes fermées (objets entiers)

---

## Code minimal

```python
import cv2
import numpy as np

image = cv2.imread('image_9.jpg')

# Étape 1 : Détection de contours (Canny)
canny = cv2.Canny(image, 50, 200)

# Étape 2 : Trouver les contours
contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# Étape 3 : Dessiner les contours sur l'image
cv2.drawContours(image, contours, -1, (255, 0, 0), 10)

cv2.imshow('Contours', image)
cv2.waitKey(0)
```

---

## Pipeline complet

```
Image originale → Canny (détection bords) → findContours (extraction) → drawContours (affichage)
```

---

## Fonction détaillée : findContours

```python
contours, hierarchy = cv2.findContours(image, mode, method)
```

| Paramètre | Valeurs | Description |
|-----------|---------|-------------|
| `image` | Image binaire | Généralement sortie de Canny ou threshold |
| `mode` | `RETR_LIST`, `RETR_EXTERNAL`, `RETR_TREE` | Mode de récupération |
| `method` | `CHAIN_APPROX_NONE`, `CHAIN_APPROX_SIMPLE` | Méthode d'approximation |

### Modes de récupération (`mode`)

| Mode | Description | Usage |
|------|-------------|-------|
| `cv2.RETR_LIST` | Récupère tous les contours sans hiérarchie | Liste simple |
| `cv2.RETR_EXTERNAL` | Récupère uniquement les contours externes | Ignorer les trous |
| `cv2.RETR_TREE` | Récupère tous avec hiérarchie complète | Objets imbriqués |

### Méthodes d'approximation (`method`)

| Méthode | Description | Usage |
|---------|-------------|-------|
| `cv2.CHAIN_APPROX_NONE` | Stocke TOUS les points du contour | Précision maximale |
| `cv2.CHAIN_APPROX_SIMPLE` | Stocke les points essentiels (coins) | Plus rapide, moins de mémoire |

### Retour : `contours`

```python
contours  # Liste de tableaux numpy
# contours[0] = premier contour = [[x1,y1], [x2,y2], [x3,y3], ...]
# contours[1] = deuxième contour
# etc.
```

---

## Fonction détaillée : drawContours

```python
cv2.drawContours(image, contours, contourIdx, color, thickness)
```

| Paramètre | Description | Exemples |
|-----------|-------------|----------|
| `image` | Image sur laquelle dessiner | `image` originale |
| `contours` | Liste des contours | Retour de findContours |
| `contourIdx` | Index du contour à dessiner | `-1` = tous, `0` = premier, `1` = deuxième... |
| `color` | Couleur (BGR) | `(255,0,0)` = bleu, `(0,255,0)` = vert |
| `thickness` | Épaisseur du trait | `2` = fin, `10` = épais, `-1` = remplissage |

---

## Analogie simple

Imagine que tu as une feuille de papier avec des formes dessinées :

1. **Canny** = Tu passes un feutre sur tous les bords visibles
2. **findContours** = Tu découpes chaque forme avec des ciseaux
3. **drawContours** = Tu recolles les découpes sur une feuille propre

Les **contours** sont comme des **pochoirs** — tu peux les réutiliser pour dessiner, compter, mesurer...

---

## Cas d'usage projets

| Projet | Usage |
|--------|-------|
| **Comptage d'objets** | Compter les pièces, les cellules, les pièces de puzzle... |
| **Mesure de surface** | Calculer l'aire de chaque contour détecté |
| **Tri de formes** | Classer les objets par forme (cercle, carré, triangle...) |
| **Détection de défauts** | Comparer contour attendu vs contour réel |
| **Robotique** | Suivre un objet en temps réel par son contour |

---

## Pièges / Astuces

⚠️ **L'ordre compte !** Toujours Canny AVANT findContours :
```python
# ✅ Bon
canny = cv2.Canny(image, 50, 200)
contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# ❌ Mauvais
contours, _ = cv2.findContours(image, ...)  # Image couleur !
```

⚠️ **Image en entrée** : findContours attend une image **binaire** (noir/blanc), pas couleur

✅ **Filtre par taille** : Ignorer les petits contours (bruit) :
```python
contours_filtres = [c for c in contours if cv2.contourArea(c) > 100]
```

✅ **Contour spécifique** : Dessiner seulement le plus grand :
```python
if contours:
    plus_grand = max(contours, key=cv2.contourArea)
    cv2.drawContours(image, [plus_grand], -1, (0,255,0), 3)
```

✅ **Couleurs BGR** : OpenCV utilise BGR, pas RGB :
- `(255,0,0)` = Bleu
- `(0,255,0)` = Vert  
- `(0,0,255)` = Rouge

---

## Exemple avancé : Analyse de contours

```python
import cv2
import numpy as np

image = cv2.imread('image_9.jpg')
canny = cv2.Canny(image, 50, 200)
contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# Analyser chaque contour
for i, contour in enumerate(contours):
    aire = cv2.contourArea(contour)           # Surface en pixels²
    perimetre = cv2.arcLength(contour, True)  # Longueur du contour
    
    print(f"Contour {i}: aire={aire:.0f}, périmètre={perimetre:.0f}")
    
    # Ne garder que les contours moyens (filtrer le bruit)
    if 100 < aire < 10000:
        cv2.drawContours(image, [contour], -1, (0,255,0), 2)

cv2.imshow('Contours filtrés', image)
cv2.waitKey(0)
```

---

## Récap visuel

```python
import cv2
import numpy as np

image = cv2.imread('objets.jpg')

# Pipeline segmentation
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
edges = cv2.Canny(blurred, 50, 150)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Affichage
resultat = image.copy()
cv2.drawContours(resultat, contours, -1, (0,255,0), 2)

print(f"{len(contours)} objets détectés")
```

---

## Section 4 ✅ TERMINÉE

Tu as maintenant les bases de la Computer Vision !
- Chargement, transformation d'images
- Détection de contours et segmentation
- Prêt pour les applications avancées (Section 5)

---

## Code source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/4.10-Image_Segmentation.py`
