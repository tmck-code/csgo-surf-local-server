#!/bin/bash

set -euxo pipefail

docker run \
  -d --net=host \
  -v "$PWD/data:/home/steam/csgo-dedicated/" \
  --name=csgo \
  -e SRCDS_TOKEN="$CSGO_GSLT" \
  -e SRCDS_NET_PUBLIC_ADDRESS=10.0.0.39 \
  -e SRCDS_IP=10.0.0.39 \
  -e SRCDS_STARTMAP="surf_utopia_njv" \
  -e SRCDS_TICKRATE=64 \
  -e SRCDS_FPSMAX=120 \
  -e SRCDS_HOSTNAME="arrakis" \
  cm2network/csgo
