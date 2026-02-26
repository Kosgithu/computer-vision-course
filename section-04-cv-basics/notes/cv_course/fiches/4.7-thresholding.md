# 4.7 - Thresholding (Seuillage)

## Concept
Convertir une image en **noir et blanc pur** (binaire) en comparant chaque pixel à un seuil.

- Pixel > seuil → **Blanc** (255)
- Pixel < seuil → **Noir** (0)

Étape obligatoire avant : conversion en **niveaux de gris** (1 valeur par pixel au lieu de 3).

## Code minimal

```python
import cv2

# Charger et convertir en gris
image = cv2.imread('image.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Seuillage binaire
ret, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```

## Fonction détaillée

```python
cv2.threshold(src, thresh, maxval, type)
```

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `src` | image en gris | Image source (1 canal, 0-255) |
| `thresh` | 0-255 | Valeur de seuil (souvent 127 = milieu) |
| `maxval` | 0-255 | Valeur si pixel > seuil (généralement 255) |
| `type` | constante | Type de seuillage (voir tableau ci-dessous) |

**Retourne :** `(retval, dst)`
- `retval` : la valeur du seuil utilisée
- `dst` : l'image binarisée

### Types de seuillage

| Type | Résultat si pixel > thresh | Résultat si pixel ≤ thresh |
|------|---------------------------|---------------------------|
| `THRESH_BINARY` | `maxval` (blanc) | `0` (noir) |
| `THRESH_BINARY_INV` | `0` (noir) | `maxval` (blanc) |
| `THRESH_TRUNC` | `thresh` (plafonné) | inchangé |
| `THRESH_TOZERO` | inchangé | `0` (noir) |
| `THRESH_TOZERO_INV` | `0` (noir) | inchangé |

## Conversion en gris

```python
cv2.cvtColor(src, code)
```

| Code | Conversion |
|------|------------|
| `COLOR_BGR2GRAY` | Couleur → Niveaux de gris |
| `COLOR_BGR2RGB` | BGR → RGB |
| `COLOR_BGR2HSV` | BGR → TSV (Teinte Saturation Valeur) |

⚠️ **Important** : OpenCV utilise **BGR** (pas RGB) ! Blue-Green-Red, pas Red-Green-Blue.

## Analogie simple

Imagine un **photocopieur en mode "noir et blanc strict"** :
- Tout ce qui est assez clair (gris clair, blanc) → blanc papier
- Tout ce qui est assez foncé (gris foncé, noir) → noir encre

Ou comme un **filtrage de spam** :
- Score > 50% → SPAM (noir)
- Score < 50% → PAS SPAM (blanc)

Le seuil (127) c'est ta barrière de décision.

## Cas d'usage projets

| Projet | Usage |
|--------|-------|
| **Scanner de documents** | Transformer photo en document propre (fond blanc, texte noir) |
| **OCR (lecture texte)** | Préparer l'image pour que l'algo reconnaisse les caractères |
| **Détection de formes** | Isoler un objet sur fond uni avant de trouver ses contours |
| **Comptage d'objets** | Séparer les objets du fond pour les compter |
| **Détection de lignes** | Pré-traitement avant transformée de Hough (détection lignes) |

## Pièges / Astuces

⚠️ **Toujours convertir en gris d'abord !** `cv2.threshold()` sur une image couleur = erreur ou résultat bizarre

⚠️ **Le seuil 127 est arbitraire** ! Il marche bien pour des images bien équilibrées, mais :
- Image sombre → tout devient noir
- Image claire → tout devient blanc
- Solution : `cv2.adaptiveThreshold()` (seuillage adaptatif par zone)

⚠️ **OpenCV = BGR, pas RGB** ! Si tu convertis depuis PIL ou matplotlib, attention à l'ordre des canaux

✅ **Astuce pour trouver le bon seuil** : Regarde l'histogramme de l'image (`plt.hist(gray.ravel(), 256, [0,256])`)
- Un pic = un groupe de pixels de même intensité
- Choisis le seuil entre deux pics

✅ **Seuillage inverse** (`THRESH_BINARY_INV`) est utile quand ton objet est plus clair que le fond

## Visualisation des types de seuillage

```
Image source (gris)    : |████████████████████| (dégradé 0→255)
                          0                  255

THRESH_BINARY (127)    : |████████████░░░░░░░░| (noir→blanc à 127)
THRESH_BINARY_INV      : |░░░░░░░░░░░░████████| (blanc→noir à 127)
THRESH_TRUNC (127)     : |████████████████████| (plafond à 127)
THRESH_TOZERO (127)    : |░░░░░░░░░░░░████████| (0 avant 127)
THRESH_TOZERO_INV (127): |████████████░░░░░░░░| (0 après 127)

Légende : █ = valeur conservée/changée  ░ = 0 (noir)
```

## Différence : Seuillage simple vs Adaptatif

| | Seuillage simple | Seuillage adaptatif |
|--|------------------|---------------------|
| **Seuil** | Même valeur pour toute l'image | Valeur calculée par zone |
| **Fonction** | `cv2.threshold()` | `cv2.adaptiveThreshold()` |
| **Usage** | Éclairage uniforme | Éclairage variable, ombres |
| **Performance** | Rapide | Plus lent |

## Prochaine étape naturelle

Après le seuillage → **détection de contours** (`cv2.findContours()`)
L'image binaire est parfaite pour trouver les bords des objets !

## Code source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/4.7-Thresholding.py`
