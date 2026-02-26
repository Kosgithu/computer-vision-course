# 4.5 - Bitwise Operations (Opérations Bit à Bit)

## Concept
Opérations logiques de base (AND, OR, XOR, NOT) appliquées aux pixels d'une image. Utile pour combiner des formes, créer des masques, extraire des régions.

## Comprendre `np.zeros()` (créer une image noire)

### Qu'est-ce que c'est ?

`np.zeros()` crée un **tableau** (matrice) rempli de **zéros**.

**En image :** Un pixel à 0 = **NOIR** (complètement sombre)

### Analogie simple

Imagine une feuille de papier quadrillée :
- Chaque case = un pixel
- `np.zeros((5, 5))` = feuille 5×5 cases, **toutes colorées en noir**

### Visualisation

```python
np.zeros((5, 5))  →  Tableau 5×5 rempli de 0

┌───┬───┬───┬───┬───┐
│ 0 │ 0 │ 0 │ 0 │ 0 │  ← ligne 0
├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 0 │ 0 │ 0 │  ← ligne 1
├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 0 │ 0 │ 0 │  ← ligne 2
├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 0 │ 0 │ 0 │  ← ligne 3
├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 0 │ 0 │ 0 │  ← ligne 4
└───┴───┴───┴───┴───┘
  0   1   2   3   4    ← colonnes

En image (niveaux de gris) :
⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛
```

### Paramètres de np.zeros()

```python
np.zeros((200, 200), np.uint8)
```

| Paramètre | Signification | Explication |
|-----------|---------------|-------------|
| `(200, 200)` | Dimensions | 200 lignes × 200 colonnes = image 200×200 pixels |
| `np.uint8` | Type de données | **u**nsigned (non signé) **int**eger **8** bits = 0 à 255 |

**Pourquoi `uint8` ?**
- C'est le format standard des images (8 bits par pixel)
- 0 = noir, 255 = blanc, entre = niveaux de gris

### Dans le code du cours

```python
rectangle = np.zeros((200, 200), np.uint8)
```
→ Crée une **image noire** de 200×200 pixels (canapé noir sur lequel on va dessiner)

```python
cv2.rectangle(rectangle, (20, 20), (180, 180), 255, -1)
```
→ Dessine un **rectangle blanc** (255 = blanc) sur cette image noire

Résultat :
```
Avant (np.zeros) :           Après (cv2.rectangle) :
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛

⬛ = 0 (noir)    ⬜ = 255 (blanc)
```

### Différence np.zeros vs np.ones

| Fonction | Crée | Utilisation typique |
|----------|------|---------------------|
| `np.zeros((h, w))` | Image **noire** (tout à 0) | Canvas vide pour dessiner dessus |
| `np.ones((h, w))` | Image remplie de **1** | Base pour créer une valeur uniforme (×valeur) |

**Astuce mnémotechnique :**
- **ZEROS** → **Z**éro = tout **noir** (comme une ardoise vierge)
- **ONES** → **U**n = point de départ pour créer une **valeur** (ex: ×120)

## Code minimal

```python
import cv2
import numpy as np

# Créer deux formes simples (noir et blanc)
rectangle = np.zeros((200, 200), np.uint8)
cv2.rectangle(rectangle, (20, 20), (180, 180), 255, -1)

circle = np.zeros((200, 200), np.uint8)
cv2.circle(circle, (100, 100), 100, 255, -1)

# Opérations bitwise
and_result = cv2.bitwise_and(rectangle, circle)
or_result = cv2.bitwise_or(rectangle, circle)
xor_result = cv2.bitwise_xor(rectangle, circle)
not_result = cv2.bitwise_not(rectangle)
```

## Rappel : Opérations logiques

| Opération | Description | Analogie |
|-----------|-------------|----------|
| **AND** | 1 seulement si les deux sont 1 | Intersection (commun aux deux) |
| **OR** | 1 si au moins un est 1 | Union (l'un ou l'autre ou les deux) |
| **XOR** | 1 si un seul est 1 (pas les deux) | Différence symétrique |
| **NOT** | Inverse (0→1, 1→0) | Négatif |

## Tables de vérité

### AND (`cv2.bitwise_and`)
| A | B | Résultat | Visualisation |
|---|---|----------|---------------|
| 0 | 0 | 0 | Noir + Noir = Noir |
| 0 | 1 | 0 | Noir + Blanc = Noir |
| 1 | 0 | 0 | Blanc + Noir = Noir |
| 1 | 1 | 1 | Blanc + Blanc = Blanc |

→ **Garde seulement la zone commune** (intersection rectangle ∩ cercle)

### OR (`cv2.bitwise_or`)
| A | B | Résultat |
|---|---|----------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

→ **Garde tout** (union rectangle ∪ cercle)

### XOR (`cv2.bitwise_xor`)
| A | B | Résultat |
|---|---|----------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

→ **Garde ce qui est différent** (union - intersection)

### NOT (`cv2.bitwise_not`)
| A | Résultat |
|---|----------|
| 0 | 1 |
| 1 | 0 |

→ **Inversion** (négatif)

## Fonctions OpenCV

```python
# AND - Intersection
cv2.bitwise_and(src1, src2, dst=None, mask=None)

# OR - Union
cv2.bitwise_or(src1, src2, dst=None, mask=None)

# XOR - Différence symétrique
cv2.bitwise_xor(src1, src2, dst=None, mask=None)

# NOT - Inversion
cv2.bitwise_not(src, dst=None, mask=None)
```

## Visualisation des résultats

Avec rectangle et cercle qui se chevauchent :

```
Rectangle:     Cercle:        AND:           OR:           XOR:
┌─────────┐    ◠─────◠        ┌──◠──┐       ┌─────────┐    ╱─────╲
│ ┌─────┐ │   ╱   ●   ╲       │ ●●● │      │◠─────◠  │   ╱   ●   ╲
│ │ ●●● │ │   │  ●●●  │  →    │ ●●● │  →   ││ ●●● │  │ → │  ○○○  │
│ │ ●●● │ │   │ ●●●●● │       └──◠──┘      ││ ●●● │◠─┘   │ ○○○○○ │
└─────────┘    ◡─────◡                      └─────◡─┘      ◡─────◡

Légende: ● = blanc (255), ○ = noir (0) dans le résultat
```

## Cas d'usage projets

| Projet | Usage |
|--------|-------|
| **Masquage (Masking)** | Garder seulement une zone d'intérêt |
| **Chroma key** | Remplacer fond vert (green screen) |
| **Détection contour** | Combiner masques |
| **Logo watermark** | Fusionner logo sur image |
| **Segmentation** | Isoler objets par couleur |

### Exemple concret : Masquage
```python
# Garder seulement le visage dans une image
mask = np.zeros(image.shape[:2], np.uint8)
cv2.circle(mask, (face_x, face_y), face_radius, 255, -1)

# AND entre image et masque = garde seulement le cercle
face_only = cv2.bitwise_and(image, image, mask=mask)
```

## Pièges / Astuces

⚠️ **Images doivent avoir la même taille** pour AND/OR/XOR
✅ **Images en niveaux de gris** (1 canal) ou couleur (3 canaux) fonctionnent
⚠️ **0 = noir, 255 = blanc** dans les masques
✅ **Le paramètre `mask`** permet d'appliquer l'opération seulement sur une zone

## Différence importante

| Méthode | Quand utiliser |
|---------|---------------|
| `cv2.add()` | Ajouter des valeurs (luminosité) |
| `cv2.bitwise_or()` | Combiner des formes/masques |

`add` = addition mathématique
`bitwise_or` = opération logique bit à bit

## Code source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/4.5-Bitwise_Operations.py`
