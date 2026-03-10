# Deep Dive : EigenFaces, FisherFaces et Amélioration de la Précision

## 🎭 EigenFaces - L'Analyse en Composantes Principales (PCA)

### Concept Fondamental

EigenFaces utilise **l'algèbre linéaire** pour réduire la dimensionnalité. Au lieu de stocker chaque pixel, on trouve les "ingrédients de base" qui composent tous les visages.

### Analogie : Le Cocktail de Visages

Imagine que tous les visages sont des cocktails :
- **EigenFace 1** = "Visage moyen" (base neutre)
- **EigenFace 2** = "Plus de nez, moins de menton"
- **EigenFace 3** = "Yeux plus écartés"
- **EigenFace N** = Variations subtiles

Chaque visage réel = Visage moyen + (0.3 × EigenFace2) + (-0.5 × EigenFace3) + ...

### Fonctionnement Mathématique

```
Dataset : 100 images de 100×100 pixels = 10,000 dimensions
                    ↓
        Calcul de la matrice de covariance
                    ↓
    Extraction des vecteurs propres (eigenvectors)
                    ↓
    Sélection des N premiers (ex: 50) = 99% variance
                    ↓
    Projection : 10,000 dims → 50 dims
```

### En Code

```python
# Création
recognizer = cv2.face.EigenFaceRecognizer_create(
    num_components=50,  # Nombre d'EigenFaces à garder
    threshold=5000      # Seuil de distance euclidienne
)

# Entraînement (même API que LBPH)
recognizer.train(faces, np.array(ids))

# Prédiction
label, confidence = recognizer.predict(face_roi)
# confidence = distance euclidienne dans l'espace réduit
```

### ⚠️ Pièges d'EigenFaces

```python
# PROBLÈME 1 : Toutes les images DOIVENT avoir la même taille
# ET être alignées (yeux au même endroit)

# ❌ Mauvais
face = cv2.resize(face, (200, 200))  # Si dataset en 100×100

# ✅ Bon - Normalisation obligatoire
face = cv2.resize(face, (100, 100))
face = cv2.equalizeHist(face)  # Normalisation histogramme

# PROBLÈME 2 : Sensible à l'éclairage
# Solution : Égalisation d'histogramme AVANT entraînement
```

---

## 🔬 FisherFaces - Analyse Discriminante Linéaire (LDA)

### La Grosse Différence

| | EigenFaces | FisherFaces |
|---|---|---|
| **Objectif** | Maximiser la variance totale | Maximiser la variance INTER-classes |
| **Focus** | "Qu'est-ce qui varie le plus ?" | "Qu'est-ce qui distingue les classes ?" |
| **Classes** | Peu importe | Doit connaître les classes |

### Explication Visuelle

```
EigenFaces voit ça :
┌─────────────────────────────────┐
│  😊  😐  😠  😊  😐  😠        │
│     "Tous ces visages sont      │
│      différents entre eux"      │
└─────────────────────────────────┘

FisherFaces voit ça :
┌─────────────────────────────────┐
│  😊Groupe A  😐Groupe B         │
│  😊Groupe A  😠Groupe C         │
│  "Comment séparer A, B et C ?"  │
└─────────────────────────────────┘
```

### Fonctionnement

```
Étape 1 : Calcul des visages moyens par classe
          μ_Madi, μ_Alice, μ_Bob
                    ↓
Étape 2 : Matrice de dispersion INTER-classes
          (Comment les classes diffèrent entre elles)
                    ↓
Étape 3 : Matrice de dispersion INTRA-classes
          (Comment les membres d'une classe varient)
                    ↓
Étape 4 : Maximiser ratio INTER/INTRA
          = Trouver les directions qui séparent 
            le mieux les classes tout en regroupant 
            les membres de chaque classe
```

### En Code

```python
recognizer = cv2.face.FisherFaceRecognizer_create(
    num_components=0,  # 0 = auto (C-1 classes, max 16)
    threshold=5000
)

# IMPORTANT : Besoin de PLUSIEURS images PAR PERSONNE
# Minimum : 2 images/personne (mais 5+ recommandé)
```

### Limitation Clé

```python
# FisherFaces ne peut pas avoir plus de composantes 
# que (nombre_de_classes - 1)

# Exemple :
# 3 personnes dans dataset → max 2 composantes
# 10 personnes → max 9 composantes
# 100 personnes → max 16 composantes (hard limit OpenCV)

# Conséquence : Ne fonctionne pas bien avec peu de classes
```

---

## 📊 Comparaison Détaillée des 3 Algorithmes

| Critère | EigenFaces | FisherFaces | LBPH |
|---------|-----------|-------------|------|
| **Images/personne** | 1 suffit | 2+ nécessaires | 1 suffit |
| **Alignement** | Strict requis | Strict requis | Flexible |
| **Éclairage** | Très sensible | Sensible | Robuste |
| **Expression** | Sensible | Moyen | Robuste |
| **Vitesse** | ⭐⭐⭐ Très rapide | ⭐⭐ Rapide | ⭐⭐⭐ Rapide |
| **Précision** | ⭐⭐ Correcte | ⭐⭐⭐ Bonne | ⭐⭐⭐ Bonne |
| **Classes** | Illimité | Max 16 comp. | Illimité |
| **Taille modèle** | Petit | Petit | Variable |

### Quand utiliser quoi ?

```python
# Scénario : Contrôle d'accès bureau, éclairage fixe, 5 employés
# → FisherFaces (meilleure discrimination entre classes)

# Scénario : Porte d'entrée, éclairage variable, 50 personnes  
# → LBPH (robustesse éclairage + pas besoin alignement)

# Scénario : Recherche rapide dans 1000+ photos
# → EigenFaces + indexation (vitesse maximale)
```

---

## 🚀 Améliorer la Précision - Guide Complet

### 1. Qualité du Dataset

#### A. Quantité d'images

```python
# ❌ Insuffisant
5 images par personne

# ✅ Minimum recommandé
20-30 images par personne

# ✅✅ Optimal
50-100 images avec variation
```

#### B. Variété des conditions

```python
dataset/
├── madi/
│   ├── madi_front_light.jpg      # Face, lumière normale
│   ├── madi_front_dark.jpg       # Face, sous-exposé
│   ├── madi_front_bright.jpg     # Face, surexposé
│   ├── madi_left_light.jpg       # 3/4 gauche
│   ├── madi_right_light.jpg      # 3/4 droite
│   ├── madi_up_light.jpg         # Regard en haut
│   ├── madi_down_light.jpg       # Regard en bas
│   ├── madi_smile.jpg            # Sourire
│   ├── madi_neutral.jpg          # Neutre
│   ├── madi_glasses.jpg          # Avec lunettes
│   └── ...
```

#### C. Prétraitement des images

```python
import cv2
import numpy as np

def preprocess_face(face_img, target_size=(200, 200)):
    """
    Pipeline de prétraitement optimal
    """
    # 1. Redimensionnement
    face = cv2.resize(face_img, target_size)
    
    # 2. Conversion niveaux de gris (si couleur)
    if len(face.shape) == 3:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    
    # 3. Égalisation d'histogramme (CLAHE = meilleur)
    # CLAHE = Contrast Limited Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    face = clahe.apply(face)
    
    # 4. Normalisation (0-255 → 0-1 ou -1 à 1)
    face = face.astype(np.float32) / 255.0
    
    # 5. Filtrage léger pour réduire le bruit
    face = cv2.GaussianBlur(face, (3, 3), 0)
    
    return face

# Application
faces_processed = [preprocess_face(f) for f in faces]
recognizer.train(faces_processed, ids)
```

### 2. Détection de Visage Améliorée

#### A. Cascade classique vs DNN

```python
# Méthode 1 : Haar Cascade (rapide, moins précis)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Méthode 2 : LBP Cascade (plus rapide, moins précis)
face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

# Méthode 3 : DNN (plus lent, très précis)
# Nécessite OpenCV avec module DNN
net = cv2.dnn.readNetFromCaffe(
    'deploy.prototxt',
    'res10_300x300_ssd_iter_140000.caffemodel'
)

def detect_face_dnn(frame):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                  (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Seuil de confiance
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            faces.append(box.astype(int))
    return faces
```

#### B. Alignement des Yeux (CRITIQUE pour Eigen/Fisher)

```python
import cv2
import numpy as np

def align_face(face_img, left_eye, right_eye, target_size=(200, 200)):
    """
    Aligne le visage pour que les yeux soient à des positions fixes.
    INDISPENSABLE pour EigenFaces et FisherFaces.
    
    left_eye, right_eye : tuples (x, y)
    """
    # Position désirée des yeux dans l'image alignée
    left_eye_target = (0.35 * target_size[0], 0.4 * target_size[1])
    right_eye_target = (0.65 * target_size[0], 0.4 * target_size[1])
    
    # Calcul de la transformation
    eyes_center = ((left_eye[0] + right_eye[0]) // 2,
                   (left_eye[1] + right_eye[1]) // 2)
    
    # Angle de rotation
    dy = right_eye[1] - left_eye[1]
    dx = right_eye[0] - left_eye[0]
    angle = np.degrees(np.arctan2(dy, dx))
    
    # Scale pour que la distance entre yeux soit constante
    current_dist = np.sqrt(dx**2 + dy**2)
    target_dist = right_eye_target[0] - left_eye_target[0]
    scale = target_dist / current_dist
    
    # Matrice de transformation
    M = cv2.getRotationMatrix2D(eyes_center, angle, scale)
    
    # Translation pour centrer
    tx = target_size[0] * 0.5 - eyes_center[0]
    ty = target_size[1] * 0.4 - eyes_center[1]
    M[0, 2] += tx
    M[1, 2] += ty
    
    # Application
    aligned = cv2.warpAffine(face_img, M, target_size)
    return aligned

# Utilisation
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def detect_and_align(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    aligned_faces = []
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        
        # Détection des yeux
        eyes = eye_cascade.detectMultiScale(face_roi, 1.1, 3)
        
        if len(eyes) >= 2:
            # Trier par position x (gauche vs droite)
            eyes = sorted(eyes, key=lambda e: e[0])
            left_eye = (x + eyes[0][0] + eyes[0][2]//2, 
                       y + eyes[0][1] + eyes[0][3]//2)
            right_eye = (x + eyes[1][0] + eyes[1][2]//2,
                        y + eyes[1][1] + eyes[1][3]//2)
            
            # Alignement
            aligned = align_face(gray, left_eye, right_eye)
            aligned_faces.append(aligned)
    
    return aligned_faces
```

### 3. Augmentation de Données

```python
import cv2
import numpy as np
from random import uniform

def augment_face(face_img, num_augmentations=5):
    """
    Génère des variations artificielles d'une image de visage.
    Permet de multiplier le dataset sans prendre de nouvelles photos.
    """
    augmented = []
    h, w = face_img.shape[:2]
    
    for _ in range(num_augmentations):
        img = face_img.copy()
        
        # 1. Rotation légère (±10°)
        angle = uniform(-10, 10)
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
        img = cv2.warpAffine(img, M, (w, h))
        
        # 2. Scaling (±10%)
        scale = uniform(0.9, 1.1)
        new_w, new_h = int(w*scale), int(h*scale)
        img = cv2.resize(img, (new_w, new_h))
        # Recadrage ou padding pour revenir à la taille originale
        if scale > 1:
            start = (new_w - w) // 2
            img = img[start:start+h, start:start+w]
        else:
            pad = (w - new_w) // 2
            img = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT)
            img = cv2.resize(img, (w, h))
        
        # 3. Brightness (±20%)
        brightness = uniform(0.8, 1.2)
        img = np.clip(img * brightness, 0, 255).astype(np.uint8)
        
        # 4. Flip horizontal (50% de chance)
        if uniform(0, 1) > 0.5:
            img = cv2.flip(img, 1)
        
        # 5. Bruit léger (optionnel)
        noise = np.random.normal(0, 5, img.shape).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        augmented.append(img)
    
    return augmented

# Utilisation
dataset_path = "dataset"
for person in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person)
    images = os.listdir(person_path)
    
    for img_name in images:
        img = cv2.imread(os.path.join(person_path, img_name), 0)
        
        # Générer 5 variations
        variations = augment_face(img, 5)
        for i, var in enumerate(variations):
            cv2.imwrite(f"{person_path}/aug_{i}_{img_name}", var)

# Résultat : 10 images → 60 images (originales + augmentées)
```

### 4. Techniques Avancées

#### A. Ensemble de Modèles (Voting)

```python
# Entraîner 3 modèles différents
lbph = cv2.face.LBPHFaceRecognizer_create()
eigen = cv2.face.EigenFaceRecognizer_create(num_components=50)
fisher = cv2.face.FisherFaceRecognizer_create()

lbph.train(faces, np.array(ids))
eigen.train(faces_aligned, np.array(ids))
fisher.train(faces_aligned, np.array(ids))

# Prédiction par vote
def ensemble_predict(face_roi, face_aligned):
    predictions = []
    confidences = []
    
    # LBPH
    label1, conf1 = lbph.predict(face_roi)
    predictions.append(label1)
    confidences.append(1.0 / (1.0 + conf1/100))  # Normaliser
    
    # Eigen
    label2, conf2 = eigen.predict(face_aligned)
    predictions.append(label2)
    confidences.append(1.0 / (1.0 + conf2/5000))
    
    # Fisher  
    label3, conf3 = fisher.predict(face_aligned)
    predictions.append(label3)
    confidences.append(1.0 / (1.0 + conf3/5000))
    
    # Vote pondéré
    from collections import Counter
    weights = Counter()
    for pred, conf in zip(predictions, confidences):
        weights[pred] += conf
    
    final_label = weights.most_common(1)[0][0]
    confidence = weights[final_label] / sum(confidences)
    
    return final_label, confidence
```

#### B. Validation Croisée

```python
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

def cross_validate(faces, labels, n_splits=5):
    """
    Évalue la robustesse du modèle avec validation croisée.
    """
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    scores = []
    
    for train_idx, test_idx in kf.split(faces):
        X_train = [faces[i] for i in train_idx]
        y_train = [labels[i] for i in train_idx]
        X_test = [faces[i] for i in test_idx]
        y_test = [labels[i] for i in test_idx]
        
        # Entraînement
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(X_train, np.array(y_train))
        
        # Test
        predictions = []
        for face in X_test:
            label, _ = recognizer.predict(face)
            predictions.append(label)
        
        score = accuracy_score(y_test, predictions)
        scores.append(score)
    
    print(f"Accuracy moyenne : {np.mean(scores):.2%} (+/- {np.std(scores):.2%})")
    return scores
```

#### C. Seuil Adaptatif

```python
class AdaptiveFaceRecognizer:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.thresholds = {}  # Seuil personnalisé par personne
        
    def train(self, faces, labels):
        self.recognizer.train(faces, np.array(labels))
        
        # Calculer le seuil optimal pour chaque personne
        for person_id in set(labels):
            person_faces = [f for f, l in zip(faces, labels) if l == person_id]
            confidences = []
            
            # Tester chaque image contre le modèle
            for face in person_faces:
                label, conf = self.recognizer.predict(face)
                confidences.append(conf)
            
            # Seuil = moyenne + 2*écart-type
            mean_conf = np.mean(confidences)
            std_conf = np.std(confidences)
            self.thresholds[person_id] = mean_conf + 2 * std_conf
    
    def predict(self, face):
        label, confidence = self.recognizer.predict(face)
        threshold = self.thresholds.get(label, 100)
        
        if confidence < threshold:
            return label, confidence, True  # Reconnu
        else:
            return None, confidence, False  # Inconnu
```

### 5. Post-Traitement

#### A. Lissage Temporel (pour vidéo)

```python
class TemporalSmoother:
    def __init__(self, buffer_size=10):
        self.buffer = []
        self.buffer_size = buffer_size
    
    def update(self, label, confidence):
        self.buffer.append((label, confidence))
        
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
        
        # Vote majoritaire pondéré par confiance
        from collections import defaultdict
        votes = defaultdict(float)
        
        for l, c in self.buffer:
            weight = 1.0 / (1.0 + c/100)  # Plus confiance élevée = poids faible
            votes[l] += weight
        
        if votes:
            best_label = max(votes, key=votes.get)
            avg_confidence = sum(c for l, c in self.buffer if l == best_label) / \
                           sum(1 for l, _ in self.buffer if l == best_label)
            return best_label, avg_confidence
        
        return label, confidence

# Utilisation dans la boucle vidéo
smoother = TemporalSmoother(buffer_size=5)

while True:
    frame = capture.read()
    face = detect_face(frame)
    
    if face is not None:
        label, confidence = recognizer.predict(face)
        smooth_label, smooth_conf = smoother.update(label, confidence)
        
        # Afficher smooth_label (plus stable)
        display_name = names.get(smooth_label, "Inconnu")
```

---

## 📈 Checklist d'Optimisation

### Avant l'entraînement
- [ ] Minimum 20 images par personne
- [ ] Variété d'éclairage, angles, expressions
- [ ] Toutes les images alignées (si Eigen/Fisher)
- [ ] Taille uniforme (ex: 200×200)
- [ ] Prétraitement : égalisation histogramme

### Pendant l'entraînement
- [ ] Augmentation de données (×5-10)
- [ ] Validation croisée pour tester
- [ ] Optimiser les hyperparamètres
- [ ] Sauvegarder le modèle

### Pendant la reconnaissance
- [ ] Aligner les visages détectés
- [ ] Même prétraitement qu'à l'entraînement
- [ ] Lissage temporel (vidéo)
- [ ] Seuil de confiance adaptatif
- [ ] Fallback "Inconnu" si doute

---

## 🎯 Résumé des Points Clés

| Problème | Solution |
|----------|----------|
| Trop peu d'images | Augmentation de données |
| Mauvais éclairage | CLAHE + variété dataset |
| Visages mal alignés | Détection yeux + alignement |
| Faux positifs | Seuil adaptatif + smoothing temporel |
| Précision insuffisante | Ensemble de modèles (voting) |
| Lenteur | Réduire résolution + LBPH |

**Règle d'or** : La qualité du dataset > l'algorithme. Un bon dataset avec LBPH battra un mauvais dataset avec FisherFaces.

---

*Document créé le 2026-03-10 - Deep dive reconnaissance faciale*
