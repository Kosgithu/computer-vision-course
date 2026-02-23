# Computer Vision Course - Notes

**Cours :** Udemy - Image Processing with OpenCV
**Section :** 4 - Image Processing Basics
**Statut :** En cours (4.5/4.10 en cours)
**Dernière session :** 2026-02-20

---

## Progression

| Cours | Titre | Statut | Fiche |
|-------|-------|--------|-------|
| 4.1 | Load, Display, Save | ✅ Fait | [fiche-4.1.md](./fiches/fiche-4.1.md) |
| 4.2 | Scaling (Resizing) | ✅ Fait | [fiche-4.2.md](./fiches/fiche-4.2.md) |
| 4.3 | Flipping | ✅ Fait | [fiche-4.3.md](./fiches/fiche-4.3.md) |
| 4.4 | Varying Brightness | ✅ Fait | [fiche-4.4.md](./fiches/fiche-4.4.md) |
| 4.5 | Bitwise Operations | 🔄 En cours | [fiche-4.5.md](./fiches/fiche-4.5.md) |
| 4.6 | Blurring & Sharpening | ⏭️ À venir | - |
| 4.7 | Thresholding | ⏭️ À venir | - |
| 4.8 | Erosion & Dilation | ⏭️ À venir | - |
| 4.9 | Edge Detection | ⏭️ À venir | - |
| 4.10 | Image Segmentation | ⏭️ À venir | - |

---

## Concepts clés vus jusqu'ici

### 4.1 - Bases
- `cv2.imread()` : Charger une image
- `cv2.imshow()` : Afficher dans une fenêtre
- `cv2.imwrite()` : Sauvegarder
- `cv2.waitKey(0)` : Attendre une touche

### 4.2 - Scaling
- `cv2.resize()` : Redimensionner
- **Interpolations :**
  - `cv2.INTER_CUBIC` : Qualité (réduction/agrandissement)
  - `cv2.INTER_AREA` : Réduction (bon résultat)
  - `cv2.INTER_LINEAR` : Défaut, rapide

### 4.3 - Flipping
- `cv2.flip(image, flipCode)`
  - `flipCode=1` : Horizontal (gauche-droite)
  - `flipCode=0` : Vertical (haut-bas)
  - `flipCode=-1` : Les deux (180°)

### 4.4 - Brightness
- `cv2.add()` : Augmenter luminosité (sature à 255)
- `cv2.subtract()` : Diminuer luminosité (sature à 0)
- `np.ones() * valeur` : Créer matrice de réglage

### 4.5 - Bitwise Operations (en cours)
- `cv2.bitwise_and()` : Intersection (commun aux deux)
- `cv2.bitwise_or()` : Union (l'un ou l'autre)
- `cv2.bitwise_xor()` : Différence (un seul)
- `cv2.bitwise_not()` : Inversion

---

## Prochaines étapes suggérées

1. Finir la section 4 (4.5 → 4.10)
2. Créer un mini-projet combinant CAO + µC + CV

### Idée de mini-projet
**Détecteur de présence caméra → contrôle servo**
- Caméra USB sur PC ou ESP32-CAM
- Détection de mouvement (frame differencing)
- Servo actionné via Pico quand détection
- Support imprimé 3D pour caméra + servo

---

## Fichiers source prof
`/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/`

## Mes codes traduits
`/home/oimadi/.openclaw/workspace/notes/cv_course/mes_codes/`
