build:
	docker build -f ops/Dockerfile -t csgo-surf .

bootstrap: build
	docker create --name csgo-surf csgo-surf
	docker cp csgo-surf:/home/steam/csgo-dedicated/csgo ./csgo
	docker rm -f csgo-surf

db/bootstrap:
	docker-compose run -v $(PWD)/csgo:/csgo surftimer-64t-db /csgo/SurfZones/Zones/REPLACE_ALL_maptier.sql
	docker-compose run -v $(PWD)/csgo:/csgo surftimer-64t-db /csgo/SurfZones/Zones/REPLACE_ALL_spawnlocations.sql
	docker-compose run -v $(PWD)/csgo:/csgo surftimer-64t-db /csgo/SurfZones/Zones/REPLACE_ALL_zones.sql

serve-64t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I | cut -d' ' -f 1) \
	CSGO_GSLT=$(CSGO_GSLT) \
		docker-compose up surftimer-64t

serve-100t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I | cut -d' ' -f 1) \
	CSGO_GSLT=$(CSGO_GSLT) \
		docker-compose up surftimer-100t

.PHONY: build bootstrap serve-64t serve-100t bootstrap
