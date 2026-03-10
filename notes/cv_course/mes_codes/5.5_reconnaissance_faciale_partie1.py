"""
5.5 - Reconnaissance Faciale - Partie 1
Création du dataset d'entraînement
====================================
Ce script capture plusieurs images d'un visage pour créer un dataset
personnel. Ces images serviront à entraîner le modèle de reconnaissance
faciale (Partie 2).

Source originale : Human_Face_Recognition-1.py (cours Udemy)
Adapté pour Raspberry Pi 5 avec picamera2
"""

import cv2
import os
from picamera2 import Picamera2
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

# Nombre d'images à capturer par personne
NB_IMAGES = 30

# Délai entre chaque capture (en millisecondes)
DELAI_CAPTURE = 100  # 100ms = 10 images max par seconde

# Taille minimale du visage (pour filtrer les détections trop petites)
MIN_FACE_SIZE = 100  # pixels

# ============================================================================
# INITIALISATION
# ============================================================================

# Saisie des informations de la personne
print("=" * 50)
print("CRÉATION DU DATASET - RECONNAISSANCE FACIALE")
print("=" * 50)
face_id = input('\nEntrez l\'ID numérique de la personne (ex: 0, 1, 2...) : ')
face_name = input('Entrez le nom de la personne : ')

# Création du dossier de destination
dataset_path = f"dataset/{face_name}"
os.makedirs(dataset_path, exist_ok=True)
print(f"\nDossier créé : {dataset_path}")

# Chargement du classificateur de visage
cascade_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    print(f"❌ Erreur : Impossible de charger {cascade_path}")
    print("Téléchargez le fichier depuis :")
    print("https://github.com/opencv/opencv/tree/master/data/haarcascades")
    exit(1)

# Initialisation de la caméra (picamera2 pour Raspberry Pi 5)
print("\nInitialisation de la caméra...")
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
))
picam2.start()
time.sleep(0.1)  # Court délai pour laisser la caméra s'initialiser

print("✅ Caméra prête !")
print(f"\n📸 Captures en cours... (0/{NB_IMAGES})")
print("Conseil : Bougez légèrement la tête pour varier les angles")
print("Appuyez sur ÉCHAP pour arrêter\n")

# ============================================================================
# CAPTURE DES IMAGES
# ============================================================================

count = 0

while count < NB_IMAGES:
    # Capture d'une frame depuis la caméra
    # picamera2 retourne une image en format RGB
    frame = picam2.capture_array()
    
    # ⚠️ CONVERSION OBLIGATOIRE : RGB → BGR
    # OpenCV travaille en BGR, picamera2 capture en RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Conversion en niveaux de gris pour la détection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Détection des visages
    # scaleFactor=1.3 : Réduction de 30% à chaque échelle
    # minNeighbors=5 : Nombre minimum de détections pour valider un visage
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(MIN_FACE_SIZE, MIN_FACE_SIZE)
    )
    
    # Traitement de chaque visage détecté
    for (x, y, w, h) in faces:
        # Incrémentation du compteur
        count += 1
        
        # Extraction de la région d'intérêt (ROI) = le visage
        # On travaille sur l'image en niveaux de gris pour la reconnaissance
        face_roi = gray[y:y+h, x:x+w]
        
        # Sauvegarde de l'image du visage
        filename = f"{dataset_path}/{count}.jpg"
        cv2.imwrite(filename, face_roi)
        
        # Affichage d'un rectangle vert autour du visage détecté
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Feedback visuel : texte au-dessus du rectangle
        cv2.putText(
            frame,
            f'Image {count}/{NB_IMAGES}',
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    
    # Affichage du compteur global en haut à gauche
    cv2.putText(
        frame,
        f'Photos: {count}/{NB_IMAGES}',
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )
    
    # Barre de progression visuelle
    bar_width = 300
    progress = int((count / NB_IMAGES) * bar_width)
    cv2.rectangle(frame, (10, 50), (10 + bar_width, 70), (50, 50, 50), -1)
    cv2.rectangle(frame, (10, 50), (10 + progress, 70), (0, 255, 0), -1)
    
    # Instructions
    cv2.putText(
        frame,
        'Bougez la tete - ECHAP pour quitter',
        (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 200),
        1
    )
    
    # Affichage de la frame
    cv2.imshow('Collecte Dataset - Reconnaissance Faciale', frame)
    
    # Attente avec vérification de la touche ÉCHAP (27)
    key = cv2.waitKey(DELAI_CAPTURE)
    if key == 27:  # ÉCHAP
        print("\n⚠️ Capture interrompue par l'utilisateur")
        break

# ============================================================================
# NETTOYAGE
# ============================================================================

# Arrêt de la caméra
picam2.stop()

# Fermeture des fenêtres
cv2.destroyAllWindows()

# Résumé
print("\n" + "=" * 50)
print("RÉSUMÉ")
print("=" * 50)
print(f"✅ Personne : {face_name} (ID: {face_id})")
print(f"✅ Images capturées : {count}/{NB_IMAGES}")
print(f"✅ Dossier : {dataset_path}")
print(f"\nProchaine étape : Exécutez le script 5.6 pour entraîner le modèle")
print("=" * 50)

# ============================================================================
# NOTES
# ============================================================================

"""
ASTUCES POUR UN BON DATASET :
-----------------------------
1. Variez les angles : face, 3/4 gauche, 3/4 droite
2. Changez l'éclairage : normal, lumière vive, ombre
3. Modifiez l'expression : neutre, sourire
4. Ajoutez des accessoires : lunettes, casquette (optionnel)
5. Bougez lentement pendant la capture

STRUCTURE DU DATASET CRÉÉ :
---------------------------
dataset/
├── nom_personne_1/
│   ├── 1.jpg
│   ├── 2.jpg
│   └── ...
└── nom_personne_2/
    ├── 1.jpg
    └── ...

PROBLÈMES FRÉQUENTS :
--------------------
- "Aucun visage détecté" : Vérifiez l'éclairage, rapprochez-vous
- "Images floues" : Restez immobile pendant la capture
- "Trop de visages" : Assurez-vous d'être seul devant la caméra
"""
