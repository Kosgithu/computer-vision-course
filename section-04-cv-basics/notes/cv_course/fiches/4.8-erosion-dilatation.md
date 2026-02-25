# 4.8 - Érosion et Dilatation (Morphologie)

## Concept
Opérations morphologiques qui modifient la **forme** des objets dans une image en jouant sur leurs contours.

| Opération | Effet | Utilisation typique |
|-----------|-------|---------------------|
| **Érosion** | Rétrécit les objets, "mange" les bords | Supprimer le bruit, séparer objets collés |
| **Dilatation** | Grossit les objets, "ajoute" aux bords | Combler trous, reconnecter morceaux d'objets |

---

## Code minimal

```python
import cv2
import numpy as np

image = cv2.imread('image_7.jpg')

# Créer un kernel (noyau) 5x5 rempli de 1
kernel = np.ones((5, 5), dtype="uint8")

# Érosion : rétrécit les objets
erosion = cv2.erode(image, kernel, iterations=1)

# Dilatation : grossit les objets
dilation = cv2.dilate(image, kernel, iterations=1)
```

---

## Le Kernel (Noyau) - Explications détaillées

### Qu'est-ce que c'est ?
Le **kernel** est une petite matrice (généralement carrée) qui définit la "zone d'action" de l'opération morphologique. C'est comme un **tampoune** ou un **cache** que l'on fait glisser sur chaque pixel de l'image.

### Création du kernel

```python
kernel = np.ones((5, 5), dtype="uint8")
```

| Paramètre | Description |
|-----------|-------------|
| `(5, 5)` | Dimensions du kernel : 5 pixels × 5 pixels |
| `dtype="uint8"` | Type unsigned 8-bit (valeurs 0-255), standard pour les images |

### Ce que contient le kernel

```
kernel 3×3 =  [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]]

kernel 5×5 =  [[1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1]]
```

Chaque `1` représente un pixel "actif" qui participe au calcul.

### Analogie du kernel

Imagine que tu as une **gomme carrée** (pour l'érosion) ou un **crayon épais** (pour la dilatation) :
- **3×3** = petite gomme/crayon → effet fin et précis
- **5×5** = gomme/crayon moyen → effet modéré
- **7×7** = grosse gomme/crayon → effet fort et grossier

> **Plus le kernel est grand, plus l'effet sera prononcé !**

### Tailles de kernel courantes

| Taille | Effet | Usage |
|--------|-------|-------|
| `3×3` | Léger | Suppression de bruit fin, détails |
| `5×5` | Moyen | Usage général (celui du cours) |
| `7×7` ou + | Fort | Grosses corrections, objets très bruités |

### Autres formes de kernel

```python
# Kernel rectangulaire (pas forcément carré)
kernel_rect = np.ones((3, 5), dtype="uint8")  # 3 lignes, 5 colonnes

# Kernel avec forme spécifique (croix)
kernel_cross = np.array([[0, 1, 0],
                         [1, 1, 1],
                         [0, 1, 0]], dtype="uint8")
```

---

## Les Itérations - Explications détaillées

### Qu'est-ce que c'est ?
Les **iterations** définissent **combien de fois** on applique l'opération (érosion ou dilatation) sur l'image. C'est comme passer plusieurs coups de gomme au même endroit.

```python
cv2.erode(image, kernel, iterations=1)   # 1 passe
cv2.erode(image, kernel, iterations=3)   # 3 passes
```

### Effet des itérations

| Itérations | Érosion résultat | Dilatation résultat |
|------------|------------------|---------------------|
| `1` | Légère réduction | Légère expansion |
| `2` | Réduction modérée | Expansion modérée |
| `3+` | Réduction forte | Expansion forte |

### Analogie des itérations

**Pour l'érosion :**
Imagine que tu grattes une étiquette sur un objet :
- `iterations=1` → Un coup de grattoir, l'étiquette est un peu abîmée
- `iterations=3` → Trois coups, l'étiquette est presque partie
- `iterations=5` → Cinq coups, tu as peut-être abîmé l'objet lui-même !

**Pour la dilatation :**
Imagine que tu dessines avec un feutre qui dégouline :
- `iterations=1` → Le trait est un peu épais
- `iterations=3` → Le trait est très épais et déborde
- `iterations=5` → C'est devenu une grosse tache !

### Formule magique

L'effet total dépend des **deux facteurs combinés** :

```
Effet total = Taille du kernel × Nombre d'itérations

Exemples équivalents :
- Kernel 5×5 + 1 itération  ≈  Kernel 3×3 + 2-3 itérations
- Kernel 3×3 + 3 itérations  ≈  Kernel 9×9 + 1 itération
```

> **Astuce :** Il vaut souvent mieux un kernel moyen avec peu d'itérations qu'un kernel énorme (meilleur contrôle).

---

## Fonction détaillée

### Érosion

```python
cv2.erode(src, kernel, iterations=1)
```

| Paramètre | Type | Description |
|-----------|------|-------------|
| `src` | ndarray | Image source (entrée) |
| `kernel` | ndarray | Matrice de convolution (généralement `np.ones()`) |
| `iterations` | int | Nombre de passes (défaut: 1) |

**Fonctionnement interne :**
Pour chaque pixel, si **TOUS** les pixels du kernel couvrent un pixel blanc (objet), le pixel reste blanc. Sinon, il devient noir (supprimé).

### Dilatation

```python
cv2.dilate(src, kernel, iterations=1)
```

**Fonctionnement interne :**
Pour chaque pixel, si **AU MOINS UN** pixel du kernel couvre un pixel blanc (objet), le pixel devient blanc (ajouté).

---

## Comparaison visuelle Érosion vs Dilatation

```
Image originale :      Après Érosion :        Après Dilatation :

    ████████              ██████                ████████████
   ████████████           ████████              ████████████████
  ██████████████          ████████             ██████████████████
   ████████████           ████████              ████████████████
    ████████              ██████                ████████████

   (objet normal)       (plus petit, net)    (plus gros, flou)
```

---

## Cas d'usage projets

| Projet | Technique | Pourquoi ? |
|--------|-----------|------------|
| **OCR** (reconnaissance texte) | Érosion puis dilatation | Nettoyer le bruit autour des caractères |
| **Comptage d'objets** | Érosion | Séparer objets collés pour les compter individuellement |
| **Détection de défauts** | Dilatation | Mettre en évidence petites rayures ou trous |
| **Préparation ML** | Les deux | Normaliser la taille des objets dans le dataset |
| **Cartographie** | Érosion | Supprimer détails parasites, garder grandes zones |

---

## Combinaison puissante : Opening & Closing

### Opening (Ouverture) = Érosion + Dilatation
```python
# Supprime le bruit en début d'image
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
```
→ Efface les petits points blancs isolés (bruit)

### Closing (Fermeture) = Dilatation + Érosion
```python
# Comble les trous dans les objets
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
```
→ Bouche les petits trous noirs dans les objets blancs

---

## Pièges / Astuces

⚠️ **Ordre des opérations compte !** Érosion puis dilatation ≠ dilatation puis érosion

⚠️ **Les deux modifient la taille** : tes objets ne feront plus la même taille après !

⚠️ **Sur images couleur** : Applique sur un canal ou convertis en niveaux de gris d'abord

✅ **Pour le bruit** : Utilise Opening (érosion → dilatation)

✅ **Pour combler trous** : Utilise Closing (dilatation → érosion)

✅ **Teste avec iterations=1 d'abord**, augmente progressivement

✅ **Kernel 3×3 ou 5×5** suffisent dans 90% des cas

---

## Récap visuel

```python
import cv2
import numpy as np

image = cv2.imread('image.jpg', 0)  # Niveaux de gris
_, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

kernel = np.ones((5, 5), np.uint8)

# Érosion = "rétrécit"
eroded = cv2.erode(binary, kernel, iterations=1)

# Dilatation = "grossit"
dilated = cv2.dilate(binary, kernel, iterations=1)

# Opening = nettoie le bruit
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# Closing = comble les trous
closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
```

---

## Code source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/4.8-Erosion_Dilation.py`
