---
title: "Fiches de Cours - OpenCV Computer Vision"
author: "Madi - Koseus"
date: "2026-02-20"
---

# FICHES DE COURS OPENCV

---

# 4.1 - Load, Display, Save (Charger, Afficher, Sauvegarder)

## Concept
Les 3 opérations de base avec OpenCV : charger, afficher, sauvegarder une image.

## Code minimal

```python
import cv2

# Charger
image = cv2.imread('image_1.jpg')

# Afficher
cv2.imshow("Original", image)
cv2.waitKey(0)  # Attend touche

# Sauvegarder
cv2.imwrite("Saved Image.jpg", image)
```

## Fonctions clés

| Fonction | Description | Paramètres |
|----------|-------------|------------|
| `cv2.imread(path)` | Charge image depuis fichier | Chemin relatif ou absolu |
| `cv2.imshow(name, img)` | Affiche dans fenêtre | Nom fenêtre, image |
| `cv2.waitKey(delay)` | Attend touche (ms) | 0 = infini |
| `cv2.imwrite(path, img)` | Sauvegarde image | Chemin, image |

## Pourquoi `cv2.waitKey()` est indispensable

**Le problème :**
Quand tu fais `cv2.imshow()`, Python affiche l'image ET continue immédiatement le script.
Sans `waitKey()`, le script finit en quelques millisecondes → la fenêtre se ferme instantanément.

**Ce que fait `waitKey()` :**
- Bloque l'exécution du programme
- Attend que tu appuies sur une touche du clavier
- Paramètre = temps d'attente maximum (en millisecondes)

| Valeur | Comportement |
|--------|-------------|
| `waitKey(0)` | Attend infiniment jusqu'à touche |
| `waitKey(1000)` | Attend 1 seconde max |
| `waitKey(5000)` | Attend 5 secondes max |

**Astuce :** Appuie sur n'importe quelle touche pour continuer. Echap (ESC) marche aussi.

---

# 4.2 - Scaling (Redimensionnement)

## Concept
Redimensionner une image avec différentes méthodes d'interpolation (estimation des valeurs entre pixels).

## Code minimal

```python
import cv2
import numpy as np

image = cv2.imread('image_2.jpg')

# Méthode 1 : Échelle relative (fx, fy)
resized = cv2.resize(image, None, fx=0.5, fy=0.5, 
                     interpolation=cv2.INTER_LINEAR)

# Méthode 2 : Taille absolue (width, height)
resized = cv2.resize(image, (600, 300), 
                     interpolation=cv2.INTER_AREA)
```

## Qu'est-ce qu'une interpolation ?

Quand tu redimensionnes une image, OpenCV doit inventer des pixels pour remplir les trous (agrandissement) ou choisir lesquels garder (réduction).

**Exemple simple :**
Tu as une image de 100×100 pixels. Tu veux la doubler → 200×200 pixels.
- Tu passes de 10 000 pixels à 40 000 pixels
- OpenCV doit créer 30 000 pixels manquants
- L'interpolation = la méthode pour calculer ces nouveaux pixels

## Interpolations

| Méthode | Quand utiliser | Qualité | Vitesse |
|---------|---------------|---------|---------|
| `cv2.INTER_LINEAR` | Défaut, général | ⭐⭐⭐ | Rapide |
| `cv2.INTER_CUBIC` | Agrandissement | ⭐⭐⭐⭐⭐ | Lent |
| `cv2.INTER_AREA` | Réduction | ⭐⭐⭐⭐ | Moyen |

**Astuce mnémo :** AREA = réduction efficace

---

# 4.3 - Flipping (Retournement Miroir)

## Concept
Retourner une image horizontalement, verticalement, ou les deux (miroir).

## Code minimal

```python
import cv2

image = cv2.imread('image_3.jpg')

# Horizontal (miroir gauche-droite)
flip_h = cv2.flip(image, 1)

# Vertical (miroir haut-bas)  
flip_v = cv2.flip(image, 0)

# Les deux (rotation 180°)
flip_both = cv2.flip(image, -1)
```

## Paramètres

| flipCode | Effet |
|----------|-------|
| `1` | Horizontal (gauche ↔ droite) |
| `0` | Vertical (haut ↔ bas) |
| `-1` | Les deux (180°) |

**Astuce mnémo :** "1 c'est comme une barre verticale" (1 = l) pour horizontal

---

# 4.4 - Luminosité (Brightness)

## Concept
Augmenter ou diminuer la luminosité d'une image en ajoutant/soustrayant une valeur à tous les pixels.

## Code minimal

```python
import cv2
import numpy as np

image = cv2.imread('image_4.jpg')

# Créer une matrice remplie de 120
matrix = np.ones(image.shape, dtype="uint8") * 120

# Augmenter luminosité
brighter = cv2.add(image, matrix)

# Diminuer luminosité
darker = cv2.subtract(image, matrix)
```

## Comprendre `np.ones()` et `np.zeros()`

**np.zeros((3, 5))** → Tableau 3×5 rempli de 0 (noir)
**np.ones((3, 5))** → Tableau 3×5 rempli de 1

**uint8** = unsigned integer 8 bits = valeurs de 0 à 255 (standard des images)

### Explication pas à pas

1. `np.ones(image.shape, dtype="uint8")` → Crée un tableau de la même taille que l'image, rempli de 1
2. `* 120` → Multiplie chaque 1 par 120 → tableau rempli de 120
3. `cv2.add(image, matrix)` → Ajoute 120 à chaque pixel (plus lumineux)
4. `cv2.subtract(image, matrix)` → Retire 120 à chaque pixel (plus sombre)

**Pourquoi cv2.add() et pas juste + ?**
- cv2.add() gère la saturation : 230 + 50 = 255 (blanc), pas 280 (erreur)

---

# 4.5 - Opérations Bitwise (AND, OR, XOR, NOT)

## Concept
Opérations logiques entre images. Utile pour combiner des formes, créer des masques.

## Comprendre `np.zeros()`

`np.zeros((200, 200), np.uint8)` crée une image NOIRE de 200×200 pixels.

- 0 = noir
- 255 = blanc

## Code minimal

```python
import cv2
import numpy as np

# Créer canvas noir et dessiner dessus
rectangle = np.zeros((200, 200), np.uint8)
cv2.rectangle(rectangle, (20, 20), (180, 180), 255, -1)

circle = np.zeros((200, 200), np.uint8)
cv2.circle(circle, (100, 100), 100, 255, -1)

# Opérations
and_result = cv2.bitwise_and(rectangle, circle)   # Intersection
or_result = cv2.bitwise_or(rectangle, circle)     # Union
xor_result = cv2.bitwise_xor(rectangle, circle)   # Différence
not_result = cv2.bitwise_not(rectangle)           # Inversion
```

## Tables de vérité

### AND (ET) - Garde la zone commune
| A | B | Résultat |
|---|---|----------|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

### OR (OU) - Garde tout
| A | B | Résultat |
|---|---|----------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

### XOR (OU exclusif) - Garde les différences
| A | B | Résultat |
|---|---|----------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

### NOT (NON) - Inverse
| A | Résultat |
|---|----------|
| 0 | 1 |
| 1 | 0 |

## Cas d'usage

- **Masquage** : Garder seulement une zone d'intérêt
- **Chroma key** : Remplacer fond vert
- **Logo watermark** : Fusionner logo sur image

---

# RÉCAPITULATIF DES FONCTIONS

| Cours | Fonction principale | À retenir |
|-------|---------------------|-----------|
| 4.1 | `cv2.imread()`, `cv2.imshow()`, `cv2.imwrite()` | Bases |
| 4.2 | `cv2.resize()` | Interpolation AREA = réduction |
| 4.3 | `cv2.flip()` | 1=h, 0=v, -1=les deux |
| 4.4 | `cv2.add()`, `cv2.subtract()` | Luminosité |
| 4.5 | `cv2.bitwise_and/or/xor/not()` | Masques |

---

**Fiches créées par Koseus le 2026-02-20**
