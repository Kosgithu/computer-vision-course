# 4.2 - Scaling (Resizing)

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

## Fonction détaillée

```python
cv2.resize(src, dsize, fx, fy, interpolation)
```

| Paramètre | Description | Exemple |
|-----------|-------------|---------|
| `src` | Image source | `image` |
| `dsize` | Taille sortie (width, height) | `(600, 300)` ou `None` |
| `fx` | Facteur X (si dsize=None) | `0.5` = moitié |
| `fy` | Facteur Y (si dsize=None) | `0.75` = 75% |
| `interpolation` | Méthode calcul | Voir ci-dessous |

## Qu'est-ce qu'une interpolation ?

Quand tu redimensionnes une image, OpenCV doit **inventer des pixels** pour remplir les trous (agrandissement) ou **choisir lesquels garder** (réduction).

**Exemple simple :**
Tu as une image de 100×100 pixels. Tu veux la doubler → 200×200 pixels.
- Tu passes de 10 000 pixels à 40 000 pixels
- OpenCV doit créer 30 000 pixels manquants
- **L'interpolation** = la méthode pour calculer ces nouveaux pixels

**Analogie :**
Imagine une grille de points (les pixels). L'interpolation, c'est comme tracer une courbe lisse entre ces points pour estimer les valeurs aux endroits où il n'y a pas de point.

## Interpolations

| Méthode | Quand utiliser | Qualité | Vitesse |
|---------|---------------|---------|---------|
| `cv2.INTER_LINEAR` | Défaut, général | ⭐⭐⭐ | Rapide |
| `cv2.INTER_CUBIC` | Agrandissement | ⭐⭐⭐⭐⭐ | Lent |
| `cv2.INTER_AREA` | Réduction | ⭐⭐⭐⭐ | Moyen |

## Astuce mnémo

> **AREA** = **A**grandissement **R**educti**E** non, **A**réduction **R**eduction **E**fficace

(AREA est pour la réduction)

## Pièges / Astuces

⚠️ **(width, height)** pas (height, width) → inversé par rapport à shape
⚠️ **fx/fy** nécessitent `dsize=None`
⚠️ **CUBIC lent** : Éviter en temps réel sur µC

## Cas d'usage projets

| Projet | Usage |
|--------|-------|
| Détection temps réel | Réduire pour accélérer traitement |
| Affichage web | Adapter taille écran |
| Dataset ML | Normaliser taille entrée |

## Prochaine utilisation
Envisager pour mini-projet caméra : réduire image avant traitement pour alléger ESP32.

## Code source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/4.2-Scaling.py`
