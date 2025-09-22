#!/bin/bash

set -euxo pipefail

docker create --name surftimer-base surftimer
docker cp surftimer-base:/home/steam .
docker rm -f surftimer-base
docker compose run \
  -it \
  surftimer-base \
  bash -c '"${STEAMCMDDIR}/steamcmd.sh" \
    +force_install_dir "${STEAMAPPDIR}" \
    +login anonymous \
    +app_update "${STEAMAPPID}" validate \
    +quit'

docker compose down --remove-orphans

