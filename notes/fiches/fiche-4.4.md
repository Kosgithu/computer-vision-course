# 4.4 - Varying Brightness (Luminosité)

## Concept
Augmenter ou diminuer la luminosité d'une image en ajoutant/soustrayant une valeur à tous les pixels.

## Code minimal

```python
import cv2
import numpy as np

image = cv2.imread('image_4.jpg')

# Créer une matrice de même taille que l'image, remplie de 120
matrix = np.ones(image.shape, dtype="uint8") * 120

# Augmenter luminosité
brighter = cv2.add(image, matrix)

# Diminuer luminosité
darker = cv2.subtract(image, matrix)
```

## Comprendre `np.ones()` et `np.zeros()` (Numpy)

### Qu'est-ce que c'est ?

`np.ones()` et `np.zeros()` sont des fonctions de la bibliothèque **Numpy** qui créent des **tableaux** (matrices) remplis de valeurs.

**Analogie simple :** C'est comme créer une grille de cases et décider ce qu'on met dedans :
- `np.zeros()` → grille remplie de **0** (noir)
- `np.ones()` → grille remplie de **1** (valeur de base)

### Visualisation

```
np.zeros((3, 5))              np.ones((3, 5))
┌───┬───┬───┬───┬───┐        ┌───┬───┬───┬───┬───┐
│ 0 │ 0 │ 0 │ 0 │ 0 │        │ 1 │ 1 │ 1 │ 1 │ 1 │
├───┼───┼───┼───┼───┤        ├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 0 │ 0 │ 0 │        │ 1 │ 1 │ 1 │ 1 │ 1 │
├───┼───┼───┼───┼───┤        ├───┼───┼───┼───┼───┤
│ 0 │ 0 │ 0 │ 0 │ 0 │        │ 1 │ 1 │ 1 │ 1 │ 1 │
└───┴───┴───┴───┴───┘        └───┴───┴───┴───┴───┘
     Tableau 3×5 rempli          Tableau 3×5 rempli
        de ZÉROS                    de UNS
```

### Paramètres expliqués

```python
np.ones((hauteur, largeur), dtype="uint8")
```

| Paramètre | Description | Exemple |
|-----------|-------------|---------|
| `(200, 200)` | **Taille** du tableau : 200 lignes × 200 colonnes | Image 200×200 pixels |
| `dtype="uint8"` | **Type** de données : entier non signé 8 bits | Valeurs 0 à 255 |

**Pourquoi `uint8` ?**
- `u` = unsigned (non signé, donc pas de négatifs)
- `int` = integer (nombre entier)
- `8` = 8 bits = 256 valeurs possibles (0 à 255)
- C'est le **standard des images** (chaque pixel = 0=noir, 255=blanc)

### Explication pas à pas du code 4.4

### 1. `np.ones(image.shape, dtype="uint8")`
- `image.shape` = récupère la taille de l'image originale → ex: `(480, 640, 3)`
- Crée un tableau de la **même taille** que l'image
- Rempli de **1** partout
- Chaque "case" contient la valeur 1

### 2. `* 120`
- Multiplie **chaque case** par 120
- Résultat : matrice remplie de **120** partout

Avant `* 120` :                    Après `* 120` :
```
┌───┬───┬───┐                      ┌────┬────┬────┐
│ 1 │ 1 │ 1 │                      │120 │120 │120 │
├───┼───┼───┤     ×120   →         ├────┼────┼────┤
│ 1 │ 1 │ 1 │                      │120 │120 │120 │
└───┴───┴───┘                      └────┴────┴────┘
```

### 3. `cv2.add(image, matrix)`
- Ajoute 120 à **chaque pixel** de l'image originale
- Pixel à 50 → 50+120 = 170 (plus clair)
- Pixel à 200 → 200+120 = 255 (blanc, saturé)

### 4. `cv2.subtract(image, matrix)`
- Soustrait 120 à chaque pixel
- Pixel à 150 → 150-120 = 30 (plus sombre)
- Pixel à 50 → 50-120 = 0 (noir, saturé)

### 3. `cv2.add(image, matrix)`
- Ajoute 120 à **chaque pixel** de l'image
- Pixel à 50 → 50+120 = 170 (plus clair)
- Pixel à 200 → 200+120 = 255 (blanc, saturé)

### 4. `cv2.subtract(image, matrix)`
- Soustrait 120 à chaque pixel
- Pixel à 150 → 150-120 = 30 (plus sombre)
- Pixel à 50 → 50-120 = 0 (noir, saturé)

## Pourquoi pas simplement `image + 50` ?

❌ `image + 50` en Python = risque de **dépassement** (overflow) mal géré
✅ `cv2.add()` = gère automatiquement la saturation (clamp entre 0 et 255)

Exemple :
- Pixel à 230 + 50 = 280 → `cv2.add()` donne **255** (blanc)
- Avec `+` Python : résultat imprévisible

## Tableau récapitulatif

| Opération | Fonction | Effet | Saturation |
|-----------|----------|-------|------------|
| Addition | `cv2.add(img, value)` | Plus lumineux | Blanc (255) |
| Soustraction | `cv2.subtract(img, value)` | Plus sombre | Noir (0) |

## Cas d'usage projets

| Projet | Usage |
|--------|-------|
| Correction photo | Sous-exposée / surexposée |
| Data augmentation | Varier luminosité pour entraînement ML |
| Vision nocturne | Augmenter contraste faible éclairage |
| Détection couleur | Normaliser éclairage avant traitement |

## Pièges / Astuces

⚠️ **Valeur trop élevée** = image complètement blanche/noire
✅ **Plage conseillée** : 30-100 pour des ajustements raisonnables
⚠️ **`uint8` obligatoire** : Sinon erreur de type

## Code source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/4.4-Varying_Brightness.py`
