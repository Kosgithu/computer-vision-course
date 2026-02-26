# Détection Temps Réel : Visage, Yeux et Nez
# Réal-time Human Face, Eyes and Nose Detection

# Import du package Computer Vision - cv2
import cv2

# Import du package Numerical Python - numpy en alias np
import numpy as np

# ═══════════════════════════════════════════════════════════════
# CHARGEMENT DES CLASSIFICATEURS HAAR CASCADE
# ═══════════════════════════════════════════════════════════════

# Charge le fichier cascade pour la détection de visage
# cv2.CascadeClassifier([nom_fichier]) 
# → Charge un modèle XML entraîné à reconnaître des formes spécifiques
face_detect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Charge le fichier cascade pour la détection des yeux
eyes_detect = cv2.CascadeClassifier('haarcascade_eye.xml')

# Charge le fichier cascade pour la détection du nez
# Note : "Noise" dans le nom du fichier = "Nose" (ne) en anglais, pas "bruit"
noise_detect = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')

# ───────────────────────────────────────────────────────────────
# VÉRIFICATION DU CHARGEMENT DES FICHIERS
# ───────────────────────────────────────────────────────────────

# Vérifie si le fichier cascade visage est bien chargé
# Si vide → lève une exception avec message d'erreur explicite
if face_detect.empty():
    raise IOError('Impossible de charger le fichier haarcascade_frontalface_alt.xml')

# Vérifie si le fichier cascade yeux est bien chargé
if eyes_detect.empty():
    raise IOError('Impossible de charger le fichier haarcascade_eye.xml')
    
# Vérifie si le fichier cascade nez est bien chargé    
if noise_detect.empty():
    raise IOError('Impossible de charger le fichier haarcascade_mcs_nose.xml')

# ═══════════════════════════════════════════════════════════════
# INITIALISATION DE LA CAPTURE VIDÉO
# ═══════════════════════════════════════════════════════════════

# Crée l'objet de capture vidéo
capture = cv2.VideoCapture(0)
# Paramètres possibles :
#   0 ou -1  → Caméra par défaut (intégrée ou première USB)
#   1        → Deuxième caméra
#   2        → Troisième caméra
#   'fichier.avi' → Lecture d'un fichier vidéo

# ═══════════════════════════════════════════════════════════════
# BOUCLE PRINCIPALE DE TRAITEMENT
# ═══════════════════════════════════════════════════════════════

# Boucle infinie jusqu'à pression de la touche Echap
while True:
    
    # ───────────────────────────────────────────────────────────
    # LECTURE D'UNE FRAME
    # ───────────────────────────────────────────────────────────
    
    # capture.read() retourne 2 valeurs :
    #   ret      : True si la frame est lue correctement, False sinon
    #   capturing : L'image capturée (numpy array)
    ret, capturing = capture.read()
    
    # ───────────────────────────────────────────────────────────
    # PRÉ-TRAITEMENT
    # ───────────────────────────────────────────────────────────
    
    # Redimensionne l'image pour accélérer le traitement
    # cv2.resize(image, taille_sortie, fx, fy, interpolation)
    #   None           → Laisse OpenCV calculer la taille
    #   fx=0.5, fy=0.5 → Réduit de moitié en largeur et hauteur
    #   INTER_AREA     → Interpolation optimale pour le rétrécissement
    resize_frame = cv2.resize(capturing, None, fx=0.5, fy=0.5, 
            interpolation=cv2.INTER_AREA)
   
    # Convertit l'image couleur (BGR) en niveaux de gris
    # Les cascades Haar fonctionnent uniquement sur du gris
    # cv2.cvtColor : Convertit entre espaces de couleur
    #   COLOR_BGR2GRAY → Bleu-Vert-Rouge vers Gris
    gray = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)

    # ───────────────────────────────────────────────────────────
    # DÉTECTION DES VISAGES
    # ───────────────────────────────────────────────────────────
    
    # Détecte les objets (visages) de différentes tailles
    # detectMultiScale(image, scaleFactor, minNeighbors)
    #
    #   scaleFactor (1.3) : Facteur de réduction entre chaque scan
    #       → 1.3 = réduit de 30% entre chaque passe
    #       → Plus petit = plus précis mais plus lent
    #       → Valeur typique : 1.1 à 1.5
    #
    #   minNeighbors (5) : Nombre minimum de rectangles voisins pour valider
    #       → Plus haut = moins de faux positifs, mais peut rater des visages
    #       → Valeur typique : 3 à 6
    face_detection = face_detect.detectMultiScale(gray, 1.3, 5)
    
    # ───────────────────────────────────────────────────────────
    # TRAITEMENT DE CHAQUE VISAGE DÉTECTÉ
    # ───────────────────────────────────────────────────────────
    
    # Parcourt tous les visages détectés
    # (x, y) : coin supérieur gauche
    # (w, h) : largeur et hauteur du rectangle
    for (x, y, w, h) in face_detection:
        
        # Dessine un rectangle rouge autour du visage
        # cv2.rectangle(image, (x1,y1), (x2,y2), couleur, épaisseur)
        #   (0,0,255) = Rouge en BGR
        #   10 = épaisseur de 10 pixels
        cv2.rectangle(resize_frame, (x, y), (x+w, y+h), (0,0,255), 10)
        
        # ───────────────────────────────────────────────────────
        # EXTRACTION DE LA ROI (Region Of Interest)
        # ───────────────────────────────────────────────────────
        
        # Extrait la zone du visage détectée (pour chercher yeux/nez dedans)
        # Syntaxe array[y début:y fin, x début:x fin]
        gray_roi = gray[y:y+h, x:x+w]           # ROI en niveaux de gris
        color_roi = resize_frame[y:y+h, x:x+w]  # ROI en couleur
       
        # ───────────────────────────────────────────────────────
        # DÉTECTION DES YEUX (dans la ROI du visage)
        # ───────────────────────────────────────────────────────
        
        # Applique le détecteur d'yeux sur la ROI en gris
        # On ne cherche les yeux QUE dans le visage → plus rapide + précis
        eye_detector = eyes_detect.detectMultiScale(gray_roi)
        
        # Dessine des rectangles bleus autour des yeux détectés
        # (eye_x, eye_y) : position relative à la ROI, pas à l'image entière !
        for (eye_x, eye_y, eye_w, eye_h) in eye_detector:
            cv2.rectangle(color_roi, 
                         (eye_x, eye_y), 
                         (eye_x + eye_w, eye_y + eye_h),
                         (255, 0, 0),  # Bleu en BGR
                         5)            # Épaisseur 5 pixels
               
        # ───────────────────────────────────────────────────────
        # DÉTECTION DU NEZ (dans la ROI du visage)
        # ───────────────────────────────────────────────────────
        
        # Applique le détecteur de nez sur la ROI en gris
        nose_detector = noise_detect.detectMultiScale(gray_roi, 1.3, 5)

        # Dessine des rectangles verts autour du nez détecté
        for (nose_x, nose_y, nose_w, nose_h) in nose_detector:
            cv2.rectangle(color_roi, 
                         (nose_x, nose_y), 
                         (nose_x + nose_w, nose_y + nose_h),
                         (0, 255, 0),  # Vert en BGR
                         5)            # Épaisseur 5 pixels

    # ───────────────────────────────────────────────────────────
    # AFFICHAGE
    # ───────────────────────────────────────────────────────────
    
    # Affiche le résultat dans une fenêtre
    cv2.imshow("Detection Temps Reel", resize_frame)

    # ───────────────────────────────────────────────────────────
    # GESTION DES ÉVÉNEMENTS CLAVIER
    # ───────────────────────────────────────────────────────────
    
    # Attend 1ms et vérifie si une touche est pressée
    # Retourne le code ASCII de la touche (ou -1 si aucune)
    c = cv2.waitKey(1)
    
    # Si la touche Echap (code 27) est pressée → sort de la boucle
    if c == 27:
        break

# ═══════════════════════════════════════════════════════════════
# NETTOYAGE (TRÈS IMPORTANT !)
# ═══════════════════════════════════════════════════════════════

# Libère la caméra (sinon elle reste "bloquée" pour d'autres programmes)
capture.release()

# Ferme toutes les fenêtres OpenCV
cv2.destroyAllWindows()

# ═══════════════════════════════════════════════════════════════
# RÉCAPITULATIF DES COULEURS
# ═══════════════════════════════════════════════════════════════
# Rouge  (0,0,255)   → Visage
# Bleu   (255,0,0)   → Yeux
# Vert   (0,255,0)   → Nez
