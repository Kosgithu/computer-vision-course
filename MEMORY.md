# Mémoire Long-Terme - Koseus

## Informations clés sur Madi
- **Nom** : Madi
- **Métier** : Technicien de maintenance (BTS CRSA)
- **Objectif** : Devenir son propre bureau d'étude (prototypes, petites machines)
- **Compétences** : CAO 3D, impression 3D, Python/MicroPython, électronique (Raspberry Pi, Arduino, ESP32)
- **En cours** : Computer Vision (cours Udemy)

## Configuration Matérielle
- **Machine** : Raspberry Pi 5
- **Stockage** : SSD NVMe Gen3 (en cours d'installation)
- **OS** : Debian GNU/Linux 13 (trixie) - 64-bit

## Workflow Udemy Computer Vision

### À chaque nouveau chapitre étudié par Madi :

1. **Récupérer le code source**
   - Source : `/home/oimadi/mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/`
   - Fichier : `[X.X-Nom].py`

2. **Traduire et enrichir**
   - Traduire tous les commentaires en français
   - Ajouter des explications sur les concepts difficiles
   - Expliquer chaque paramètre des fonctions
   - Ajouter des sections "Analogie simple" et "Pièges/Astuces"

3. **Créer la fiche de révision**
   - Destination workspace : `/home/oimadi/.openclaw/workspace/notes/cv_course/fiches/[X.X]-nom-du-sujet.md`
   - Format : suivre `4.3-retournement.md`
   - Sections : Concept, Code minimal, Fonction détaillée, Analogie, Cas d'usage, Pièges, Code source prof

4. **Mettre à jour GitHub**
   - Repo : `Kosgithu/computer-vision-course`
   - Placer dans : `section-XX-nom/notes/cv_course/fiches/` et `mes_codes/`
   - Commit + push
   - Mettre à jour README.md (racine) avec progression

### Structure du repo GitHub

```
computer-vision-course/
├── section-04-cv-basics/           # ✅ Section 4 complète
│   ├── notes/cv_course/fiches/     # Fiches de révision
│   └── notes/cv_course/mes_codes/  # Codes traduits FR
├── section-05-real-world-apps/     # ⏳ À venir
├── section-06-neural-networks/     # ⏳ À venir
├── section-07-assignments/         # ⏳ À venir
└── section-08-ai-resources/        # ⏳ À venir
```

### Structure workspace (local)

```
/home/oimadi/
├── mes_ressources_md/Ressources_Udemy/Codes/Course_codes_image/  (source prof)
└── .openclaw/workspace/notes/cv_course/
    ├── fiches/                    (fiches de révision - temporaire)
    └── mes_codes/                 (codes traduits FR - temporaire)
```

## Progression Computer Vision

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

### Section 5 : Real-world Applications (1/6)

| Chapitre | Sujet | Status |
|----------|-------|--------|
| 5.1 | Détection Visage/Yeux/Nez (VideoCapture + Haar) | ✅ |
| 5.2 | Détection de voitures dans une vidéo | ⏳ |
| 5.3 | Détection de piétons CCTV | ⏳ |
| 5.4 | Détection temps réel avec ORB | ⏳ |
| 5.5 | Reconnaissance faciale - Partie 1 | ⏳ |
| 5.6 | Reconnaissance faciale - Partie 2 | ⏳ |

### Section 6 : Neural Networks on Colab (0/5)

| Chapitre | Sujet | Status |
|----------|-------|--------|
| 6.1 | Introduction to Google Colab | ⏳ |
| 6.2 | What is a Neural Network? | ⏳ |
| 6.3 | Building your first Neuron | ⏳ |
| 6.4 | Training a Model for Image Classification | ⏳ |
| 6.5 | Testing the Model with New Data | ⏳ |

### Section 7 : Assignments (0/2)

| Chapitre | Sujet | Status |
|----------|-------|--------|
| 7.1 | Automated Security Camera | ⏳ |
| 7.2 | Solution and Discussion | ⏳ |

### Section 8 : AI Resources (0/3)

| Chapitre | Sujet | Status |
|----------|-------|--------|
| 8.1 | Recommended Books and Articles | ⏳ |
| 8.2 | Future Learning Path | ⏳ |
| 8.3 | Conclusion | ⏳ |

**Total : 11/26 chapitres (42%)**

## GitHub Token

- **Fichier** : `~/.config/openclaw/github-token`
- **Permissions** : 600 (lecture/écriture propriétaire uniquement)
- **Scopes** : repo, workflow
- **Utilisation** : Définir `GH_TOKEN` avant d'utiliser `gh`

```bash
export GH_TOKEN=$(cat ~/.config/openclaw/github-token)
gh repo create ...
```

---
*Dernière mise à jour : 2026-02-25*
