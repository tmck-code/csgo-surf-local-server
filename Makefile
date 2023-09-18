build:
	docker build -f ops/Dockerfile -t surftimer .

plugin/bootstrap:
	docker create --name csgo-surf csgo-surf
	docker cp csgo-surf:/home/steam/csgo-dedicated/csgo ./csgo
	docker rm -f csgo-surf

db/bootstrap:
	docker-compose run -v $(PWD)/csgo:/csgo surftimer-64t bash -c "sleep 3 && mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) mysql < /csgo/scripts/mysql-files/fresh_install.sql"
	docker-compose run -v $(PWD)/csgo:/csgo surftimer-64t bash -c "sleep 3 && mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) mysql < /csgo/SurfZones/Zones/REPLACE_ALL_maptier.sql"
	docker-compose run -v $(PWD)/csgo:/csgo surftimer-64t bash -c "sleep 3 && mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) mysql < /csgo/SurfZones/Zones/REPLACE_ALL_spawnlocations.sql"
	docker-compose run -v $(PWD)/csgo:/csgo surftimer-64t bash -c "sleep 3 && mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) mysql < /csgo/SurfZones/Zones/REPLACE_ALL_zones.sql"

bootstrap: build plugin/bootstrap db/bootstrap

serve-64t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I | cut -d' ' -f 1) \
	CSGO_GSLT=$(CSGO_GSLT) \
		docker-compose up surftimer-64t

serve-100t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I | cut -d' ' -f 1) \
	CSGO_GSLT=$(CSGO_GSLT) \
		docker-compose up surftimer-100t

.PHONY: build bootstrap plugin/bootstrap db/bootstrap serve-64t serve-100t
