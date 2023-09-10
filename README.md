# csgo-surf-local-server

## bootstrapping

Bootstrapping/building this will

1. build the base docker image containing all dependencies
    1. including an initial csgo dir
    2. with all the git plugin dirs in the correct location
2. run a mysql container bind-mounted to the host, and mysql database/tables required for SurfTimer
3. run a container using the base image, which copies the csgo dir out onto the host
    1. this copies/overrides any cfgs etc. from the ops/configs dir
4. run everything with docker-compose up

## running

```shell
# for a regular 64 tick server
docker-compose up

# for a 100 tick server
SRCDS_TICKRATE=100 docker-compose up
```

## TODO

- [x] create separate cfg/docker-compose definitions for 64/85/100 tick rates
- [ ] get all plugins working
  - [ ] ramp fix
  - [x] movement unlocker working
  - [ ] map chooser, with config
- [ ] account for all required cfg files, add to ops/configs and mount them correctly

## Debug commands

### The rcon utility

```shell
./ops/rcon_command 'sm plugins list'
```

## Additional Config

### `surf_server.cfg`

> see `config/surf_server.cfg`

This CFG file contains all of the required vars to make surf work.

### The "Ramp Glitch" Fix

> see `config/ramp_glitch_patch/`

Without this, the player can encounter sudden and complete loss of velocity when
changing direction on a ramp

- from https://forums.alliedmods.net/showthread.php?t=301075
    Old 09-07-2017 , 10:22   [CSGO] Ramp slope fix (from Momentum Mod)
    Reply With Quote #1
    Ramp slope fix
    Prevent players from stopping dead on (most?) ramps.

    **Slope movement**
    The Momentum Mod team claims to have fixed players having their velocity reset on slopes like surf ramps.
    User fatalis opened an issue on their GitHub repository describing his testings which would eventually be merged into
    the game.

    SM9 asked for ways to port it to CSGO in IRC the other day, so here we go.

    The plugin does exactly the same as the sv_ramp_fix ConVar in Momentum Mod, removing the code to reset player velocity
    when the game thinks they're inside a wall or suddently move in the opposite direction.

    PHP Code:
    ```php
    VectorCopy(vec3_origin, mv->m_vecVelocity);
    ```
    The only significant difference in CSGO is client prediction. The patch is only performed on the server, so clients
    will still predict getting stuck but continue on when they notice the server has a different opinion.

    **View punch**
    The CGameMovement::TryPlayerMove function checks if the player was slowed down significantly and simulates
    slamming into a wall with some effects on the client - including a huge view punch shaking the camera.

    The plugin optionally is using DHooks to hook and block CGameMovement:layerRoughLandingEffects. The problem in CSGO is
    again that the view punch code is in the client as well, so it'll predict a view punch again, but reset shortly after.
    (Momentum Mod added a convar and moved it all to the server side)

    Installation
    ```text
    Upload ramp_slope_fix.games.txt into your gamedata folder.
    Upload ramp_slope_fix.smx into your plugins folder.
    Optionally install DHooks for the view punch hook.
    ```

    It seems there are still issues on high tickrate servers, but others confirmed it working. Please see if this works
    for you and post your findings!

    Attached Files
    ```text
    File Type: txt	ramp_slope_fix.games.txt (2.4 KB, 1355 views)
    File Type: sp	Get Plugin or Get Source (ramp_slope_fix.sp - 995 views - 4.6 KB)
    File Type: smx	ramp_slope_fix.smx (6.4 KB, 1167 views)
    ```

### HUD Speedometer

> from https://github.com/kiljon/extended-speed-meter

### CSGO Movement Unlocker

> from https://forums.alliedmods.net/showthread.php?t=255298
