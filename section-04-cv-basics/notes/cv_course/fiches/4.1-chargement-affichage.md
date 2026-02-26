# 4.1 - Load, Display, Save

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
Quand tu fais `cv2.imshow()`, Python affiche l'image **et continue immédiatement** le script.
Sans `waitKey()`, le script finit en quelques millisecondes → la fenêtre se ferme instantanément.

**Ce que fait `waitKey()` :**
- **Bloque l'exécution** du programme
- **Attend que tu appuies sur une touche** du clavier
- **Paramètre** = temps d'attente maximum (en millisecondes)

| Valeur | Comportement |
|--------|-------------|
| `waitKey(0)` | Attend **infiniment** jusqu'à touche |
| `waitKey(1000)` | Attend **1 seconde** max |
| `waitKey(5000)` | Attend **5 secondes** max |

**Exemple concret :**
```python
cv2.imshow("Mon Image", image)  # Fenêtre s'ouvre
cv2.waitKey(0)                   # Bloque ici ← tu vois l'image
# ← Le code reprend ICI quand tu appuies sur une touche
```

**💡 Astuce :** Appuie sur n'importe quelle touche pour continuer. Echap (ESC) marche aussi.

## Pièges / Astuces

⚠️ **Chemin relatif** : Le script s'exécute depuis le dossier courant
⚠️ **`waitKey(0)` bloquant** : Sans ça, la fenêtre s'affiche 1ms et disparaît
✅ **Extensions supportées** : .jpg, .png, .bmp, .tiff...

## Quand l'utiliser
- Chargement initial de toute image
- Debug rapide (affichage intermédiaire)
- Export résultat traitement

## Liens projets
- [VMC IR](../projets/vmc-ir.md) : Pas utilisé (pas besoin d'affichage)
- [Lampe WiFi](../projets/lampe-wifi.md) : Pas utilisé
