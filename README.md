# Computer Vision Course 🎓

Repository personnel de suivi du cours Udemy "Computer Vision" de Madi.

## Structure du Cours

| Section | Sujet | Progression |
|---------|-------|-------------|
| 4 | CV Basics | ✅ Complète |
| 5 | Real-world Applications | 🔄 En cours |
| 6 | Neural Networks on Colab | ⏳ À venir |
| 7 | Assignments | ⏳ À venir |
| 8 | AI Resources | 📂 Vide |

---

## Organisation

```
computer-vision-course/
├── section-04-cv-basics/
│   ├── notes/cv_course/fiches/     # Fiches de révision
│   └── notes/cv_course/mes_codes/  # Codes traduits FR
├── section-05-real-world-apps/
│   ├── notes/cv_course/fiches/
│   └── notes/cv_course/mes_codes/
├── section-06-neural-networks/
├── section-07-assignments/
└── section-08-ai-resources/
```

---

## Chapitres Complétés

### Section 4 : Fondamentaux OpenCV
| Chapitre | Sujet | Status |
|----------|-------|--------|
| 4.1 | Chargement et affichage | ✅ |
| 4.2 | Redimensionnement | ✅ |
| 4.3 | Retournement | ✅ |
| 4.4 | Luminosité | ✅ |
| 4.5 | Opérations Bitwise | ✅ |
| 4.6 | Flou et Netteté | ✅ |
| 4.7 | Thresholding | ✅ |
| 4.8 | Érosion et Dilatation | ✅ |
| 4.9 | Détection de contours | ✅ |
| 4.10 | Segmentation | ✅ |

### Section 5 : Applications Réelles (en cours)
| Chapitre | Sujet | Status |
|----------|-------|--------|
| 5.1 | Détection Visage/Yeux/Nez (VideoCapture + Haar) | ✅ |
| 5.2 | Détection de voitures dans une vidéo | ✅ |
| 5.3 | Détection de piétons CCTV | ⏳ |
| 5.4 | Détection temps réel avec ORB | ⏳ |
| 5.5 | Reconnaissance faciale - Partie 1 | ⏳ |
| 5.6 | Reconnaissance faciale - Partie 2 | ⏳ |

---

## Matériel Utilisé

- **Machine** : Raspberry Pi 5
- **Stockage** : SSD NVMe Gen3
- **OS** : Debian GNU/Linux 13 (trixie) 64-bit
- **Caméra** : Module Caméra CSI Raspberry Pi

---

## Notes Importantes

⚠️ **Pour la caméra sur Pi 5** : `cv2.VideoCapture(0)` ne fonctionne pas à cause d'un bug GStreamer. Utiliser `picamera2` pour capturer et `cv2` pour le traitement.

Exemple dans `section-05-real-world-apps/notes/cv_course/mes_codes/5.1-detection-visage-yeux-nez.py`

---

*Dernière mise à jour : 2026-03-04*
