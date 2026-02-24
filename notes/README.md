# Computer Vision Course - Notes

**Cours :** Udemy - Image Processing with OpenCV  
**Section :** 4 - Image Processing Basics  
**Statut :** En cours (4.1 à 4.7 complétés)  
**Dernière mise à jour :** 2026-02-24

---

## Structure

```
cv_course/
├── fiches/                 # Fiches de révision traduites
│   ├── fiche-4.1.md        # Chargement et affichage
│   ├── fiche-4.2.md        # Redimensionnement
│   ├── fiche-4.3.md        # Retournement
│   ├── fiche-4.4.md        # Luminosité
│   ├── fiche-4.5.md        # Opérations Bitwise
│   ├── fiche-4.6.md        # Flou et Netteté
│   └── fiche-4.7.md        # Seuillage (Thresholding)
└── mes_codes/              # Codes Python traduits
    ├── 4.1-Load_Display_Save_FR.py
    ├── 4.2-Scaling_FR.py
    ├── 4.3-Flipping_FR.py
    ├── 4.4-Varying_Brightness_FR.py
    ├── 4.5-Bitwise_Operations_FR.py
    ├── 4.5-Bitwise_Operations_FR_CLAIR.py
    ├── 4.6-Blurring_Sharpening_FR.py
    └── 4.7-Thresholding_FR.py
```

---

## Progression

| Cours | Titre | Statut | Fiche |
|-------|-------|--------|-------|
| 4.1 | Load, Display, Save | ✅ Fait | [fiche-4.1.md](./cv_course/fiches/fiche-4.1.md) |
| 4.2 | Scaling (Resizing) | ✅ Fait | [fiche-4.2.md](./cv_course/fiches/fiche-4.2.md) |
| 4.3 | Flipping | ✅ Fait | [fiche-4.3.md](./cv_course/fiches/fiche-4.3.md) |
| 4.4 | Varying Brightness | ✅ Fait | [fiche-4.4.md](./cv_course/fiches/fiche-4.4.md) |
| 4.5 | Bitwise Operations | ✅ Fait | [fiche-4.5.md](./cv_course/fiches/fiche-4.5.md) |
| 4.6 | Blurring & Sharpening | ✅ Fait | [fiche-4.6.md](./cv_course/fiches/fiche-4.6.md) |
| 4.7 | Thresholding | ✅ Fait | [fiche-4.7.md](./cv_course/fiches/fiche-4.7.md) |
| 4.8 | Erosion & Dilation | ⏭️ À venir | - |
| 4.9 | Edge Detection | ⏭️ À venir | - |
| 4.10 | Image Segmentation | ⏭️ À venir | - |

---

## Concepts clés

### 4.1 - Bases
- `cv2.imread()` : Charger une image
- `cv2.imshow()` : Afficher dans une fenêtre
- `cv2.imwrite()` : Sauvegarder
- `cv2.waitKey(0)` : Attendre une touche

### 4.2 - Scaling
- `cv2.resize()` : Redimensionner
- **Interpolations :** `INTER_CUBIC`, `INTER_AREA`, `INTER_LINEAR`

### 4.3 - Flipping
- `cv2.flip(image, flipCode)`
  - `flipCode=1` : Horizontal
  - `flipCode=0` : Vertical
  - `flipCode=-1` : 180°

### 4.4 - Brightness
- `cv2.add()` / `cv2.subtract()` : Modifier luminosité
- `np.ones() * valeur` : Créer matrice de réglage

### 4.5 - Bitwise Operations
- `cv2.bitwise_and()` : Intersection
- `cv2.bitwise_or()` : Union
- `cv2.bitwise_xor()` : Différence
- `cv2.bitwise_not()` : Inversion

### 4.6 - Blurring & Sharpening
- `cv2.blur()` : Flou moyenne
- `cv2.GaussianBlur()` : Flou gaussien
- `cv2.filter2D()` : Convolution personnalisée (sharpening)

### 4.7 - Thresholding
- `cv2.cvtColor(img, COLOR_BGR2GRAY)` : Conversion gris
- `cv2.threshold()` : Seuillage binaire
  - `THRESH_BINARY`, `THRESH_BINARY_INV`
  - `THRESH_TRUNC`, `THRESH_TOZERO`

---

## Fichiers source

**Codes originaux (prof) :**
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/`

**Mes codes traduits :**
`./cv_course/mes_codes/`

---

## Guides complémentaires

- **[Hugging Face Inference API](../guides/huggingface-inference-api.md)** : Guide complet pour utiliser l'API Hugging Face (génération d'images et texte avec IA)
