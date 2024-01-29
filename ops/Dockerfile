FROM cm2network/csgo:sourcemod

USER root

RUN apt update \
    && apt install -y git unzip default-mysql-client

USER steam

# Download the most recent version of the surftimer:dev branch (https://github.com/surftimer/SurfTimer/archive/refs/heads/dev.zip)
ENV SURFTIMER_ZIP https://github.com/surftimer/SurfTimer/archive/b9c860942b8a55b7e36c244264f53c4e6d13a32b.zip
WORKDIR /tmp
RUN curl -L $SURFTIMER_ZIP -o surftimer.zip \
    && unzip surftimer.zip -d /home/steam/csgo-dedicated/csgo/ \
    && rm surftimer.zip

WORKDIR /home/steam/csgo-dedicated/csgo/

RUN git clone https://github.com/Sayt123/SurfZones

# install updated files for the "csgo_movement_unlocker" plugin
# (get >260 speed when sliding on ground for prestrafe)
ADD ops/plugins/csgo_movement_unlocker/csgo_movement_unlocker.smx addons/sourcemod/plugins/
ADD ops/plugins/csgo_movement_unlocker/csgo_movement_unlocker.games.txt addons/sourcemod/gamedata/

# install the "ramp slope fix (from momentum mod)
# https://forums.alliedmods.net/showthread.php?t=301075
ADD ops/plugins/ramp_slope_fix/ramp_slope_fix.smx addons/sourcemod/plugins/
ADD ops/plugins/ramp_slope_fix/ramp_slope_fix.games.txt addons/sourcemod/gamedata/

# install databases config file
ADD ops/configs/server/databases.cfg addons/sourcemod/configs/
# install mapchooser config file
ADD ops/configs/server/st-mapchooser.cfg cfg/sourcemod/

# install surftimer cfg
ADD ops/configs/server/64t/surftimer.cfg cfg/
# install custom surf server cfg
ADD ops/configs/server/64t/surf_server.cfg cfg/

ADD ops/entry.sh /home/steam/

WORKDIR /home/steam/
