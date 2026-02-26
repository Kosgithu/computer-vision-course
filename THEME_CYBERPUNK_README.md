# 🎨 Personnalisation Cyberpunk - Raspberry Pi

Configuration effectuée le 2026-02-21 pendant que Madi dormait. 😴

---

## ✅ Ce qui a été installé

### Logiciels
- **Inkscape** - Logiciel de dessin vectoriel (demandé par Madi)
- **LXAppearance** - Pour changer facilement les thèmes GTK
- **Feh** - Visionneur d'images et gestionnaire de fonds d'écran

### Thème Cyberpunk Neon
- **Source** : GitHub - Roboron3042/Cyberpunk-Neon
- **Palette** : Cyan néon (#0abdc6), Magenta (#d300c4), Orange (#f57800)
- **Emplacement** : `~/.themes/oomox-cyberpunk-neon/`

### Fond d'écran
- **Source** : Unsplash (libre de droits)
- **Emplacement** : `~/Pictures/wallpapers/sci-fi-city-green.jpg`
- **Résolution** : 1920×1240
- **Style** : Ville futuriste sci-fi cyberpunk néon (inspiré de Freepik)

### Terminal personnalisé
- **Prompt cyberpunk** avec couleurs néon
- **Couleurs personnalisées** pour `ls` (dossiers en cyan, fichiers en orange/magenta)
- **Configuration** : Dans `~/.bashrc`

---

## 🚀 Comment utiliser

### Changer le thème visuellement
```bash
lxappearance
```
→ Sélectionne le thème "oomox-cyberpunk-neon" dans l'onglet "Widget"

### Réappliquer le fond d'écran
```bash
feh --bg-scale ~/Pictures/wallpapers/sci-fi-city-green.jpg
```

### Lancer le script complet
```bash
bash ~/.openclaw/workspace/apply-cyberpunk-theme.sh
```

---

## 🎨 Palette de couleurs Cyberpunk

| Couleur | Hex | Usage |
|---------|-----|-------|
| Cyan néon | `#0abdc6` | Texte principal, dossiers |
| Magenta | `#d300c4` | Accent, liens |
| Orange | `#f57800` | Fichiers exécutables, warning |
| Rouge | `#ff0000` | Erreurs |
| Bleu foncé | `#000b1e` | Fond terminal |
| Bleu | `#123e7c` | Éléments secondaires |

---

## 📁 Fichiers créés

```
~/.themes/oomox-cyberpunk-neon/          # Thème GTK
~/Pictures/wallpapers/cyberpunk-wallpaper.jpg  # Fond d'écran
~/.openclaw/workspace/apply-cyberpunk-theme.sh # Script d'application
~/.bashrc                                # Config terminal (modifié)
~/.config/lxsession/LXDE-pi/desktop.conf # Config session LXDE
```

---

## 💡 Astuces

### Pour revenir au thème par défaut
```bash
# Dans lxappearance, sélectionne "PiXflat" ou "Adwaita"
```

### Changer le fond d'écran
Remplace l'image dans `~/Pictures/wallpapers/` et relance le script.

### Personnaliser le prompt
Édite `~/.bashrc` et modifie la ligne `export PS1=...`

---

## 🔧 Désinstallation

Si tu veux revenir en arrière :
```bash
# Supprimer le thème
rm -rf ~/.themes/oomox-cyberpunk-neon

# Restaurer bashrc (si tu as une sauvegarde)
cp ~/.bashrc.backup ~/.bashrc

# Réinstaller thème par défaut
sudo apt install --reinstall raspberrypi-ui-mods
```

---

*Personnalisation faite avec 💜 par Koseus*
