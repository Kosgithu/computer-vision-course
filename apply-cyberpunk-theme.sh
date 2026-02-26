#!/bin/bash
# Script de personnalisation Cyberpunk pour Raspberry Pi

# Couleurs Cyberpunk Neon
# Cyan: #0abdc6
# Magenta: #d300c4  
# Orange: #f57800
# Rouge: #ff0000
# Bleu foncé: #000b1e
# Bleu: #123e7c

echo "🎨 Application du thème Cyberpunk Neon..."

# Définir le fond d'écran (ville futuriste sci-fi néon)
WALLPAPER="$HOME/Pictures/wallpapers/sci-fi-city-green.jpg"
if [ -f "$WALLPAPER" ]; then
    # Pour PCManFM (gestionnaire de fichiers LXDE)
    pcmanfm --set-wallpaper="$WALLPAPER" 2>/dev/null
    
    # Pour feh (si installé)
    feh --bg-scale "$WALLPAPER" 2>/dev/null
    
    echo "✅ Fond d'écran cyberpunk (cityscape) appliqué"
fi

# Définir le thème GTK
export GTK_THEME="oomox-cyberpunk-neon"

# Mettre à jour les paramètres GTK
if command -v gsettings &> /dev/null; then
    gsettings set org.gnome.desktop.interface gtk-theme "oomox-cyberpunk-neon" 2>/dev/null
    gsettings set org.gnome.desktop.wm.preferences theme "oomox-cyberpunk-neon" 2>/dev/null
fi

# Configuration LXDE/LXAppearance
mkdir -p ~/.config/lxsession/LXDE-pi
cat > ~/.config/lxsession/LXDE-pi/desktop.conf << EOF
[Session]
window_manager=openbox

[GTK]
sNet/ThemeName=oomox-cyberpunk-neon
sNet/IconThemeName=oomox-cyberpunk-neon
sGtk/FontName=Noto Sans 10
EOF

echo "✅ Thème GTK Cyberpunk configuré"
echo ""
echo "📝 Pour appliquer complètement :"
echo "   1. Déconnecte-toi et reconnecte-toi, OU"
echo "   2. Lance : lxappearance et sélectionne 'oomox-cyberpunk-neon'"
echo ""
echo "🖼️  Fond d'écran : ~/Pictures/wallpapers/cyberpunk-wallpaper.jpg"
echo "🎨 Thème : ~/.themes/oomox-cyberpunk-neon/"
