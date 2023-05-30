#!/bin/bash

set -euxo pipefail

DEST_DIR="${1:-$PWD}"
CSGO_DIR="$DEST_DIR/csgo"
SOURCEMOD_DIR="$CSGO_DIR/addons/sourcemod"
PLUGINS_DIR="$SOURCEMOD_DIR/plugins"
GAMEDATA_DIR="$SOURCEMOD_DIR/gamedata"

mkdir -p "$CSGO_DIR"

# plugins ---------------------------------------
function print_starting()   { printf "\e[0;31m${1}\e[0m" ; }
function print_complete()   { printf "\e[0;32m${1}\e[0m" ; }
function print_installing() { printf "\e[0;33m${1}\e[0m" ; }

# directories ------------------------------------

ROOT_DATA_DIR="${1:-${PWD}}"
CSGO_DIR="$ROOT_DATA_DIR/csgo"

dirs=(
  csgo
  csgo/bin/linux64
  csgo/addons/metamod
  csgo/addons/sourcemod
  csgo/addons/stripper
  csgo/cfg/sourcemod
  csgo/expressions
  csgo/maps/graphs
  csgo/materials/panorama
  csgo/models
  csgo/panorama
  csgo/resource/ui
  csgo/scenes
  csgo/scripts
  csgo/sound
)

function createDirs() {
  local csgo_dir="$1"
  local subdirs="$2"

  mkdir -vp "$root_data_dir"
  cd "$csgo_dir"
  echo ${subdirs[@]} | xargs -n1 mkdir -vp
  print_complete "✔' creates all required dirs under $CSGO_DIR"
}

# recommended for SurfTimer ---------------------

# PLUGINS ---------------------------------------
# most plugin repos contain a dir or zip that is intended to be copied straight
# to somewhere in the server CSGO config path.
# These locations are always under the csgo/ config dir, but vary per-repo

# Momentum Mod Ramp Glitch Fix
function MomSurfFix() {
  print_starting "MomSurfFix (Momentum Mod Ramp Glitch Fix)"

  rm -rf MomSurfFix
  git clone git@github.com:GAMMACASE/MomSurfFix.git
  cp -Rv MomSurfFix/addons "$CSGO_DIR"
  rm -rf MomSurfFix
  print_complete "MomSurfFix"
}

# CSGO Movement Unlocker
# I've included the files in this repo, they are originally sourced from this
# AlliedModders forum post: https://forums.alliedmods.net/showthread.php?t=255298
function CSGOMovementUnlocker() {
  print_starting "CSGO Movement Unlocker"
  plugin_dir="$PWD/ops/plugins/csgo_movement_unlocker"
  cp -v "$plugin_dir/csgo_movement_unlocker.games.txt" "$CSGO_DIR/gamedata"
  cp -v "$plugin_dir/csgo_movement_unlocker.smx" "$CSGO_DIR/plugins"
  print_complete "CSGO Movement Unlocker"
}

function SurfTimerMapChooser() {
  # map chooser
  print_starting "SurfTimer Map Chooser"
  zip_fname="SurfTimer-MC-v2.0.2.zip"
  wget \
    https://github.com/surftimer/SurfTimer-Mapchooser/releases/download/2.0.2/$zip_fname
  unzip $zip_fname -d "$CSGO_DIR"

  rm $zip_fname
  print_complete "SurfTimer Map Chooser"
}

# The SurfTimer plugin
# HUD speedometer, saveloc/teleport, zones/stages/times (stored in mysql db)
function SurfTimer() {
  print_starting "SurfTimer"
  zip_fname="SurfTimer.1.1.4.914.6a563cd.SM1.11.zip"
  wget "https://github.com/surftimer/SurfTimer/releases/download/1.1.4/$zip_fname"
  unzip $zip_fname -d "$CSGO_DIR"

  rm $zip_fname
  print_complete "SurfTimer"CSGO_DIR
}

PLUGINS=(
  CSGOMovementUnlocker
  MomSurfFix
  SurfTimer
  SurfTimerMapChooser
)

function install_plugins() {
  for installer in "${PLUGINS[@]}"; do
    print_installing "$installer"
    $installer
  done
}

# metadata -----------------------------000000000

function zone_coordinates() {
  # SurfTimer zone coordinates for most surf maps
  echo "- SurfTimer zone coordinates"
  git clone https://github.com/Sayt123/SurfZones
}

# config files ----------------------------------

function install_csf_files() {
  local csgo_dir="$1"

  # - install server cfg file
  cp -v config/surf_server.cfg "$csgo_dir/cfg/"
  print_complete "surf_server.cfg config file"

  # - install the surftimer cfg file
  mkdir -p "$csgo_dir/cfg/sourcemod/surftimer/"
  cp -v config/surftimer.cfg "$csgo_dir/cfg/sourcemod/surftimer/"
  print_complete "surftimer.cfg config file"
}

# run --------------------------------------------

install_plugins
install_csf_files "$CSGO_DIR"
