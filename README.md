# csgo-surf-local-server

> _A local CSGO SurfTimer™ server in docker_

- This repository contains the tools to run a local CSGO SurfTimer™ server in docker.
- This can bootstrap a new one with all the required dependencies. or using an existing `csgo` directory.

---

- [csgo-surf-local-server](#csgo-surf-local-server)
  - [TODO](#todo)
  - [setting up the server](#setting-up-the-server)
    - [bootstrap commands](#bootstrap-commands)
    - [admin users](#admin-users)
  - [Admin \& Debug commands](#admin--debug-commands)
    - [The rcon utility](#the-rcon-utility)
  - [Additional Config](#additional-config)
    - [`surf_server.cfg`](#surf_servercfg)
    - [The GSLT token](#the-gslt-token)
  - [map zones](#map-zones)
    - [adding your own map zones](#adding-your-own-map-zones)
  - [Resources](#resources)

## TODO

- [x] create separate cfg/docker-compose definitions for 64/85/100 tick rates
- [x] get all plugins working
  - [x] ramp fix
  - [x] movement unlocker working
- [ ] configure all plugins
  - [ ] map chooser, with config

## setting up the server

> Before running the server, you'll need a GSLT token (see [The GSLT token](#the-gslt-token))

### bootstrap commands

```shell
# create a new csgo config directory (csgo-data/) and mysql data directory
# (mysql_64t) inside the repository
DB_PASSWORD=psswd make bootstrap

# run a 64 tick server using the data/ directory (or any existing csgo dir)
CSGO_GSLT=your_token_here make serve-64t

# run a 100 tick server using the data/ directory (or any existing csgo dir)
# this uses a separate DB to 64 tick server to preserve your records
CSGO_GSLT=your_token_here make serve-100t
```

### admin users

> There is an excelled community wiki here that details adding admins: https://wiki.alliedmods.net/Adding_Admins_(SourceMod)


When you launch the server you'll find that you can't run `!zone` or similar commands, as there aren't any admins configured.

1. In your CSGO client, open the console and run `status`, which will output something like this:
  ```shell
  # userid name uniqueid connected ping loss state rate
  #47 "ESL - GOTV" BOT active 24
  # 70 "username" STEAM_1:1:xxxyxyxyxyx 02:06 33 0 active 128000
  #end
  ```
  1. Grab the "uniqueid" for your user, e.g. `STEAM_1:1:xxxyxyxyxyx`
2. Edit the admin file `csgo-data/csgo/addons/sourcemod/configs/admins_simple.ini`
  1. Add the line `"STEAM_1:1:xxxyxyxyxyx" "@Full Admins"`
  2. You can double-check the admin group name by looking in `csgo-data/csgo/addons/sourcemod/configs/admin_groups.cfg`
3. Call `sm_reloadadmins` by _either_
  1. Using the CSGO console and running `rcon sm_reloadadmins`, or
  2. Running the rcon script:
    ```shell
    RCON_PASSWORD=XXX RCON_HOST=123.123.123.123 ./ops/scripts/rcon_command 'sm_reloadadmins'
    ```

## Admin & Debug commands

### The rcon utility

```shell
./ops/rcon_command 'sm plugins list'
```

## Additional Config

### `surf_server.cfg`

> see `config/surf_server.cfg`

This CFG file contains all of the required vars to make surf work.

### The GSLT token

The GSLT token is required to run the server. The Makefile (and docker-compose) expects this to be accessible via the environment variable `CSGO_GSLT`

In order to create a GSLT token, navigate to this page, login and follow the prompts to create a game server account and token: https://steamcommunity.com/dev/managegameservers

## map zones

### adding your own map zones

https://github.com/Sayt123/SurfZones/pull/2#issuecomment-1630978597

```
When manually zoning like you did here, you'd want to raise your zones quite a bit on both ends. Start zones you usually want to encapsulate the info_teleport_destination entity where players spawn. You can see them with !itd. This is also where you can find other spawns like the bonus!

Most modern maps/mappers also use hookzones to make zoning easier as well. A trigger_multiple entity that's given a name like mapstart | cp1 | bonus1start | bonus1end. Using the !hookzone menu you can actually hook a map or bonus zone TO that trigger shape the mapper made.

(Hard to see in the picture but with !triggers enabled you can see the trigger_multiple's shape this hookzone is using.)

...

Other than that on linear maps like this you also would want to add a few Checkpoint zones evenly spaced between the start and end zones.

...
```

## Resources

- There's an excellent community developer guide for CSGO dedicated servers
  - https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive/Dedicated_Servers
- How to add your own map zones
  - https://github.com/Sayt123/SurfZones/pull/2#issuecomment-1630978597
- How to run CSGO via Steam on Linux
  - https://github.com/ValveSoftware/csgo-osx-linux/issues/3291#issuecomment-1741956737