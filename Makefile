build:
	docker build -f ops/Dockerfile -t surftimer .

plugin/bootstrap:
	docker rm -f csgo-surf
	docker create --name csgo-surf surftimer
	docker cp csgo-surf:/home/steam/csgo-dedicated/ ./csgo-data
	docker rm -f csgo-surf

db/bootstrap:
	docker-compose up -d surftimer-64t
	# wait for the database to be ready
	until mysqladmin status -h 127.0.0.1 -u root -ppsswd; do sleep 1; done
	# bootstrap the database
	docker exec -it surftimer-64t bash -c "mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) surftimer < /home/steam/csgo-dedicated/csgo/scripts/mysql-files/fresh_install.sql"
	docker exec -it surftimer-64t bash -c "mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) surftimer < /home/steam/csgo-dedicated/csgo/SurfZones/Zones/REPLACE_ALL_maptier.sql"
	docker exec -it surftimer-64t bash -c "mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) surftimer < /home/steam/csgo-dedicated/csgo/SurfZones/Zones/REPLACE_ALL_spawnlocations.sql"
	docker exec -it surftimer-64t bash -c "mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) surftimer < /home/steam/csgo-dedicated/csgo/SurfZones/Zones/REPLACE_ALL_zones.sql"
	docker-compose down

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
