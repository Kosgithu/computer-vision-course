# 4.3 - Flipping (Retournement)

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

## Fonction détaillée

```python
cv2.flip(src, flipCode)
```

| Paramètre | Valeur | Effet |
|-----------|--------|-------|
| `flipCode` | `0` | Retournement **vertical** (haut ↔ bas) |
| `flipCode` | `1` | Retournement **horizontal** (gauche ↔ droite) |
| `flipCode` | `-1` | **Les deux** (équivalent à rotation 180°) |

## Analogie simple

Imagine ton image sur du papier calque :
- **flipCode = 1** (horizontal) : Tu retournes le calque comme une page de livre → gauche et droite inversés
- **flipCode = 0** (vertical) : Tu retournes le calque à l'envers → haut et bas inversés
- **flipCode = -1** : Tu retournes dans les deux sens → image complètement inversée (180°)

## Cas d'usage projets

| Projet | Usage |
|--------|-------|
| Data augmentation (ML) | Créer plus d'images d'entraînement en retournant |
| Selfie caméra | Corriger l'effet miroir des webcams |
| Symétrie objet | Vérifier si un objet est symétrique |
| Correction orientation | Photos prises dans le mauvais sens |

## Pièges / Astuces

⚠️ **flipCode = 1** pour horizontal → mémoriser : "**1** c'est comme une barre vertica**l**" (1 = l)
⚠️ **Ne modifie pas** l'image originale (retourne une copie)
✅ **Très rapide** : simple réarrangement de pixels, pas de calcul lourd

## Différence avec rotation

| Opération | Résultat |
|-----------|----------|
| `cv2.flip(image, 1)` | Miroir (gauche-droite inversé) |
| `cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)` | Tourne de 90° |

Flip ≠ Rotation ! Flip c'est un miroir, rotation c'est pivoter.

## Code source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/4.3-Flipping.py`
