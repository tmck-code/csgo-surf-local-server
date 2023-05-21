#!/bin/bash

set -euo pipefail

CSGO_DIR="$PWD/data/csgo"
SOURCEMOD_DIR="$CSGO_DIR/addons/sourcemod"
PLUGINS_DIR="$SOURCEMOD_DIR/plugins"
GAMEDATA_DIR="$SOURCEMOD_DIR/gamedata"

# Ramp Glitch Fix
echo "- Ramp Glitch Fix"
cp -v "$PWD/config/ramp_glitch_patch/ramp_slope_fix.games.txt" "$GAMEDATA_DIR"
cp -v "$PWD/config/ramp_glitch_patch/ramp_slope_fix.smx" "$PLUGINS_DIR"

# CSGO Movement Unlocker
echo "- CSGO Movement Unlocker"
cp -v "$PWD/config/csgo_movement_unlocker/csgo_movement_unlocker.games.txt" "$GAMEDATA_DIR"
cp -v "$PWD/config/csgo_movement_unlocker/csgo_movement_unlocker.smx" "$PLUGINS_DIR"

# Momentum Mod Ramp Glitch Fix
echo "- Momentum Mod Ramp Glitch Fix"
git clone gitgithub.com:GAMMACASE/MomSurfFix.git
cp -Rv MomSurfFix/addons "$CSGO_DIRPATH"
rm -rf MomSurfFix

# install surf cfg file
echo "- install surf cfg file"
cp -v "config/surf_server.cfg" "$CSGO_DIR/cfg/"

