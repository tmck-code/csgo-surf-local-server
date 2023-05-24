#!/bin/bash

set -euo pipefail

CSGO_DIR="$PWD/data/csgo"
SOURCEMOD_DIR="$CSGO_DIR/addons/sourcemod"
PLUGINS_DIR="$SOURCEMOD_DIR/plugins"
GAMEDATA_DIR="$SOURCEMOD_DIR/gamedata"

# plugins ---------------------------------------
# most plugin repos contain a dir or zip that is intended to be copied straight
# to somewhere in the server CSGO config path.
# These locations are always under the csgo/ config dir, but vary per-repo

# recommended/required for SurfTimer ------------

# Momentum Mod Ramp Glitch Fix
echo "- Momentum Mod Ramp Glitch Fix"
git clone gitgithub.com:GAMMACASE/MomSurfFix.git
cp -Rv MomSurfFix/addons "$CSGO_DIRPATH"
rm -rf MomSurfFix

# CSGO Movement Unlocker
# I've included the files in this repo, they are originally sourced from the
# AlliedModders forum post here:
# https://forums.alliedmods.net/showthread.php?t=255298
echo "- CSGO Movement Unlocker"
cp -v "$PWD/config/csgo_movement_unlocker/csgo_movement_unlocker.games.txt" "$GAMEDATA_DIR"
cp -v "$PWD/config/csgo_movement_unlocker/csgo_movement_unlocker.smx" "$PLUGINS_DIR"

# map chooser
echo "- SurfTimer Map Chooser"
wget https://github.com/surftimer/SurfTimer-Mapchooser/releases/download/2.0.2/SurfTimer-MC-v2.0.2.zip

# The SurfTimer plugin
# HUD speedometer
# saveloc/teleport
# zones/stages, stored in mysql db
# timer, times saved to mysql db
# and more!
echo "- SurfTimer"
wget https://github.com/surftimer/SurfTimer/releases/download/1.1.4/SurfTimer.1.1.4.914.6a563cd.SM1.11.zip

# SurfTimer zone coordinates for most surf maps
echo "- SurfTimer zone coordinates"
git clone https://github.com/Sayt123/SurfZones

# config files ----------------------------------

# install server cfg file
# - this contains
echo "- surf_server.cfg config file"
cp -v config/surf_server.cfg "$CSGO_DIR/cfg/"

echo "- surftimer.cfg config file"
mkdir -p "$CSGO_DIR/cfg/sourcemod/surftimer/"
cp -v config/surftimer.cfg "$CSGO_DIR/cfg/sourcemod/surftimer/"

