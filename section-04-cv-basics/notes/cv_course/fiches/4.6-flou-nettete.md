# 4.6 - Blurring (Flou) et Sharpening (Netteté)

## Concept
**Blurring** : Lisser l'image en moyennant les pixels voisins → réduit le bruit, adoucit les détails.
**Sharpening** : Accentuer les différences entre pixels voisins → renforce les contours et détails.

Ces deux opérations sont basées sur la **convolution** : on fait glisser un "masque" (noyau/kernel) sur l'image et on calcule une nouvelle valeur pour chaque pixel.

## Code minimal

```python
import cv2
import numpy as np

image = cv2.imread('image_5.jpg')

# BLURRING - Flou par moyenne
blur = cv2.blur(image, (9, 9))  # Noyau 9×9

# SHARPENING - Netteté avec noyau personnalisé
kernel = np.array([[-1, -1, -1], 
                   [-1,  9, -1], 
                   [-1, -1, -1]])
sharpened = cv2.filter2D(image, -1, kernel)
```

## Fonction détaillée - Blurring

```python
cv2.blur(src, ksize)
```

| Paramètre | Type | Description |
|-----------|------|-------------|
| `src` | image | Image source (numpy array) |
| `ksize` | tuple | Taille du noyau `(largeur, hauteur)` - **doit être impair** |

**Exemples :**
- `(3, 3)` = flou léger (moyenne sur 9 pixels)
- `(9, 9)` = flou prononcé (moyenne sur 81 pixels)

## Fonction détaillée - Sharpening

```python
cv2.filter2D(src, ddepth, kernel)
```

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `src` | image | Image source |
| `ddepth` | `-1` | Profondeur sortie (-1 = même que source) |
| `kernel` | array | Noyau de convolution (numpy array) |

**Noyau de sharpening classique :**
```
|-1  -1  -1|
|-1   9  -1|
|-1  -1  -1|
```
→ Centre amplifié (9), voisins soustraits (-1) = contours ressortent

## Analogie simple

**Blurring = Vue floue sans lunettes**
Imagine que tu retires tes lunettes : les détails disparaissent, tout devient "moyenné". Plus le noyau est grand = plus tu es myope = plus c'est flou.

**Sharpening = Lunettes qui accentuent les contrastes**
Tu mets des lunettes qui rendent les contours plus nets. Le centre du noyau (9) c'est "regarde le pixel principal", les -1 autour c'est "soustrais ses voisins" → si y'a une différence (bord), elle est amplifiée.

**La convolution = Tampon encreur**
Tu prends un tampon (le noyau), tu l'appuies sur chaque pixel de l'image, et tu calcules la valeur moyenne/poids selon le tampon. Tu déplaces le tampon pixel par pixel.

## Cas d'usage projets

| Projet | Blurring | Sharpening |
|--------|----------|------------|
| **Réduction de bruit** | ✅ Flou avant traitement | ❌ Amplifie le bruit |
| **Détection de contours** | ✅ Pré-traitement idéal | ❌ Crée faux contours |
| **Effet artistique** | ✅ Arrière-plan flou (bokeh) | ✅ Détails criards |
| **Retouche photo** | ✅ Peau lissée | ✅ Yeux/trait nets |
| **OCR (texte)** | ✅ Réduit artefacts scan | ✅ Texte plus lisible |
| **Data augmentation** | ✅ Variantes d'images | ✅ Variantes d'images |

## La Convolution expliquée simplement

La convolution c'est une **opération de voisinage** :

1. On place un petit carré (noyau) sur un pixel
2. On multiplie chaque valeur du noyau par le pixel correspondant
3. On additionne tout → ça donne la nouvelle valeur du pixel central
4. On déplace le noyau d'un pixel et on recommence

**Exemple avec noyau 3×3 tout à 1/9 (blur) :**
```
Image :        Noyau :         Calcul nouveau pixel centre :
|10 20 10|    |1/9 1/9 1/9|   (10+20+10 + 20+30+20 + 10+20+10) / 9
|20 30 20|  × |1/9 1/9 1/9| = 150 / 9 = 16.6 ≈ 17
|10 20 10|    |1/9 1/9 1/9|
```
→ Le centre valait 30, il vaut maintenant 17 (moyenne des voisins)

## Pièges / Astuces

⚠️ **Taille impaire obligatoire** : `(3,3)`, `(5,5)`, `(9,9)`... Pas de `(4,4)` !
⚠️ **Sharpening excessif** = artefacts blancs/noirs autour des contours (halo)
⚠️ **Ordre des opérations** : Toujours blur AVANT sharpening si tu fais les deux
⚠️ **filter2D** : Le noyau doit être un `numpy.array`, pas une liste Python
⚠️ **Type du noyau** : Utiliser `dtype=np.float32` pour les noyaux avec négatifs

✅ **Astuce mémotechnique** pour le noyau sharpening :
```
|-1 -1 -1|
|-1  X -1|   où X = 9 (car il y a 8 cases à -1 autour, et -8 + 9 = 1)
|-1 -1 -1|       → total = 1 pour conserver la luminosité
```

✅ **Checker la somme du noyau** :
- Somme = 1 → luminosité conservée
- Somme > 1 → image plus claire
- Somme < 1 → image plus sombre

## Autres types de flou (bonus)

| Fonction | Usage spécifique |
|----------|------------------|
| `cv2.GaussianBlur(img, (5,5), 0)` | Flou naturel, réduction bruit gaussien |
| `cv2.medianBlur(img, 5)` | Anti-bruit "sel et poivre" (points isolés) |
| `cv2.bilateralFilter(img, 9, 75, 75)` | Flou qui préserve les bords (lent mais quali) |

## Différence Blur vs Sharpening

| Aspect | Blurring | Sharpening |
|--------|----------|------------|
| **Effet** | Lisse, adoucit | Accentue, crispe |
| **Noyau** | Tous positifs (moyenne) | Positif au centre, négatifs autour |
| **Usage** | Réduire bruit, pré-traitement | Post-traitement, effet visuel |
| **Risque** | Perte de détails | Amplification du bruit, artefacts |

**Règle d'or** : 
```
Image originale → [Blur] → [Traitement] → [Sharpening] → Résultat
```
On floute d'abord pour nettoyer, on sharpen à la fin pour retrouver la netteté.

## Code source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/4.6-Blurring_Sharpening.py`
