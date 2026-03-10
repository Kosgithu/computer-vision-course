"""
5.6 - Reconnaissance Faciale - Partie 2
Entraînement et reconnaissance temps réel
=========================================
Ce script utilise le dataset créé en Partie 1 pour entraîner un modèle
LBPH (Local Binary Patterns Histograms), puis effectue la reconnaissance
faciale en temps réel.

Source originale : Human_Face_Recognition-2.py (cours Udemy)
Adapté pour Raspberry Pi 5 avec picamera2
"""

import cv2
import os
import numpy as np
from picamera2 import Picamera2
import time

# ============================================================================
# PARTIE 1 : ENTRAÎNEMENT DU MODÈLE
# ============================================================================

def train_model():
    """
    Entraîne le modèle LBPH sur le dataset créé précédemment.
    Retourne le recognizer entraîné et le dictionnaire des noms.
    """
    print("=" * 50)
    print("ENTRAÎNEMENT DU MODÈLE LBPH")
    print("=" * 50)
    
    # Création du reconnaisseur LBPH
    # LBPH = Local Binary Patterns Histograms
    # Robuste aux variations d'éclairage
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # Chargement du classificateur de visage
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    # Listes pour stocker les visages et leurs IDs
    faces = []      # Images de visages
    ids = []        # IDs numériques correspondants
    names = {}      # Dictionnaire ID → Nom
    
    # Parcours du dossier dataset
    dataset_path = "dataset"
    
    if not os.path.exists(dataset_path):
        print(f"❌ Erreur : Le dossier '{dataset_path}' n'existe pas")
        print("Exécutez d'abord le script 5.5 pour créer le dataset")
        return None, None
    
    print(f"\nChargement du dataset depuis '{dataset_path}'...")
    
    current_id = 0
    
    # Pour chaque personne dans le dataset
    for person_name in sorted(os.listdir(dataset_path)):
        person_path = os.path.join(dataset_path, person_name)
        
        # Ignorer les fichiers, ne garder que les dossiers
        if not os.path.isdir(person_path):
            continue
        
        # Attribution d'un ID numérique
        names[current_id] = person_name
        print(f"\n📁 {person_name} (ID: {current_id})")
        
        # Compteur d'images pour cette personne
        image_count = 0
        
        # Chargement de toutes les images de cette personne
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            
            # Vérification que c'est bien une image
            if not img_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                continue
            
            # Lecture de l'image en niveaux de gris
            face_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            
            if face_img is None:
                print(f"  ⚠️ Impossible de lire {img_name}")
                continue
            
            # Ajout à la liste d'entraînement
            faces.append(face_img)
            ids.append(current_id)
            image_count += 1
        
        print(f"  ✓ {image_count} images chargées")
        current_id += 1
    
    # Vérification qu'on a bien des données
    if len(faces) == 0:
        print("\n❌ Erreur : Aucune image trouvée dans le dataset")
        return None, None
    
    print(f"\n📊 Total : {len(faces)} images pour {len(names)} personne(s)")
    
    # Entraînement du modèle
    print("\n🧠 Entraînement en cours...")
    recognizer.train(faces, np.array(ids))
    
    # Sauvegarde du modèle entraîné
    model_path = 'trainer.yml'
    recognizer.save(model_path)
    print(f"✅ Modèle sauvegardé : {model_path}")
    
    return recognizer, names

# ============================================================================
# PARTIE 2 : RECONNAISSANCE TEMPS RÉEL
# ============================================================================

def recognize_faces(recognizer, names):
    """
    Effectue la reconnaissance faciale en temps réel avec la caméra.
    """
    print("\n" + "=" * 50)
    print("RECONNAISSANCE TEMPS RÉEL")
    print("=" * 50)
    print("Appuyez sur ÉCHAP pour quitter\n")
    
    # Chargement du classificateur de visage
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    # Initialisation de la caméra
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    ))
    picam2.start()
    time.sleep(0.1)
    
    # Seuil de confiance
    # Plus le score est BAS, plus la correspondance est bonne
    # < 50 : Très bonne correspondance
    # 50-100 : Bonne correspondance
    # > 100 : Douteux / inconnu
    CONFIDENCE_THRESHOLD = 100
    
    while True:
        # Capture depuis la caméra
        frame = picam2.capture_array()
        
        # ⚠️ CONVERSION RGB → BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Conversion en niveaux de gris pour la détection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Détection des visages
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(100, 100)
        )
        
        # Traitement de chaque visage détecté
        for (x, y, w, h) in faces:
            # Extraction du visage (ROI)
            face_roi = gray[y:y+h, x:x+w]
            
            # Prédiction avec le modèle entraîné
            # Retourne : (ID prédit, niveau de confiance)
            id_pred, confidence = recognizer.predict(face_roi)
            
            # ⚠️ IMPORTANT : Avec LBPH, plus le confidence est BAS, mieux c'est !
            # C'est l'inverse de l'intuition habituelle
            
            if confidence < CONFIDENCE_THRESHOLD:
                # Visage reconnu
                name = names.get(id_pred, "Inconnu")
                color = (0, 255, 0)  # Vert
                confidence_text = f"{confidence:.0f}"
            else:
                # Visage non reconnu ou inconnu
                name = "Inconnu"
                color = (0, 0, 255)  # Rouge
                confidence_text = f"{confidence:.0f}"
            
            # Dessin du rectangle autour du visage
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Affichage du nom et du score de confiance
            label = f'{name} ({confidence_text})'
            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )
            
            # Affichage de la barre de confiance
            bar_width = w
            confidence_normalized = min(confidence / 150, 1.0)  # 0-1
            bar_fill = int(bar_width * (1 - confidence_normalized))
            
            # Barre de fond (grise)
            cv2.rectangle(
                frame,
                (x, y + h + 5),
                (x + bar_width, y + h + 15),
                (50, 50, 50),
                -1
            )
            # Barre de confiance (verte si bonne, rouge si mauvaise)
            bar_color = (0, 255, 0) if confidence < CONFIDENCE_THRESHOLD else (0, 0, 255)
            cv2.rectangle(
                frame,
                (x, y + h + 5),
                (x + bar_fill, y + h + 15),
                bar_color,
                -1
            )
        
        # Informations affichées
        cv2.putText(
            frame,
            f"Personnes connues : {len(names)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
        cv2.putText(
            frame,
            "ECHAP pour quitter",
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            1
        )
        
        # Affichage de la frame
        cv2.imshow('Reconnaissance Faciale - LBPH', frame)
        
        # Vérification de la touche ÉCHAP
        if cv2.waitKey(1) == 27:
            break
    
    # Nettoyage
    picam2.stop()
    cv2.destroyAllWindows()
    print("\n✅ Reconnaissance terminée")

# ============================================================================
# PROGRAMME PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    # Étape 1 : Entraînement
    recognizer, names = train_model()
    
    if recognizer is None:
        print("\n❌ Impossible de continuer sans modèle entraîné")
        exit(1)
    
    # Étape 2 : Reconnaissance
    # Option : demander confirmation avant de lancer
    input("\nAppuyez sur ENTRÉE pour démarrer la reconnaissance...")
    recognize_faces(recognizer, names)

# ============================================================================
# EXPLICATIONS TECHNIQUES
# ============================================================================

"""
ALGORITHME LBPH (Local Binary Patterns Histograms)
-------------------------------------------------

1. Pour chaque pixel, on regarde ses 8 voisins
2. On compare chaque voisin avec le pixel central
3. Si voisin > centre → 1, sinon → 0
4. On obtient un code binaire de 8 bits (0-255)
5. On fait un histogramme de ces codes pour chaque région
6. On compare les histogrammes pour reconnaître

AVANTAGES :
- Robuste aux variations d'éclairage
- Ne nécessite pas d'alignement strict
- Rapide à l'entraînement et à la prédiction

INCONVÉNIENTS :
- Moins précis que le deep learning sur grands datasets
- Sensibles aux expressions faciales

INTERPRÉTATION DU CONFIDENCE :
------------------------------
LBPH retourne une distance (mesure de dissimilarité)

Confidence = 0    → Match parfait (identique)
Confidence < 50   → Excellente correspondance
Confidence < 100  → Bonne correspondance
Confidence > 100  → Douteux / probablement inconnu

Plus c'est BAS, mieux c'est !

AMÉLIORATIONS POSSIBLES :
-------------------------
1. Augmenter le dataset (50+ images par personne)
2. Varier les conditions (éclairage, angles)
3. Utiliser l'alignement des yeux avant reconnaissance
4. Ajouter un lissage temporel (vidéo)
5. Combiner avec EigenFaces ou FisherFaces (voting)

STRUCTURE DES FICHIERS :
-----------------------
.
├── dataset/              # Images d'entraînement
│   ├── personne_1/
│   └── personne_2/
├── trainer.yml           # Modèle entraîné (créé par ce script)
└── 5.6_reconnaissance_faciale_partie2.py
"""
