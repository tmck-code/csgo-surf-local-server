# csgo-surf-local-server

> _A local CSGO SurfTimer™ server in docker_

- This repository contains the tools to run a local CSGO SurfTimer™ server in docker.
- This can bootstrap a new one with all the required dependencies. or using an existing `csgo` directory.

---

- [csgo-surf-local-server](#csgo-surf-local-server)
  - [commands](#commands)
  - [TODO](#todo)
  - [Debug commands](#debug-commands)
    - [The rcon utility](#the-rcon-utility)
  - [Additional Config](#additional-config)
    - [`surf_server.cfg`](#surf_servercfg)
    - [The GSLT token](#the-gslt-token)

---

## commands

> Before running the server, you'll need a GSLT token (see [The GSLT token](#the-gslt-token))

```shell
# create a new csgo config directory (data/) and mysql data directory
# (mysql_64t) inside the repository
make bootstrap

# run a 64 tick server using the data/ directory (or any existing csgo dir)
make serve-64t

# run a 100 tick server using the data/ directory (or any existing csgo dir)
# this uses a separate DB to 64 tick server to preserve your records
make serve-100t
```

## TODO

- [x] create separate cfg/docker-compose definitions for 64/85/100 tick rates
- [ ] get all plugins working
  - [x] ramp fix
  - [x] movement unlocker working
  - [ ] map chooser, with config

## Debug commands

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
