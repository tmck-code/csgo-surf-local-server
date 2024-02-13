build:
	docker build -f ops/Dockerfile -t surftimer .

plugin/bootstrap:
	docker rm -f csgo-surf
	docker create --name csgo-surf surftimer
	docker cp csgo-surf:/home/csgo/server/csgo ./csgo-data-tmp/
	docker rm -f csgo-surf
	cp -Rv ./csgo-data-tmp/* ./csgo-data/csgo/

db/bootstrap:
	# inject the db password into the sourcemod config
	@sed -i "s/YOUR_PASSWORD/$(DB_PASSWORD)/g" csgo-data/csgo/addons/sourcemod/configs/databases.cfg

	docker-compose up -d surftimer-64t
	# wait for the database to be ready
	until mysqladmin status -h 127.0.0.1 -u root -p$(DB_PASSWORD); do sleep 1; done
	# bootstrap the database
	docker exec -it surftimer-64t bash -c "mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) surftimer < /home/csgo/server/csgo/scripts/mysql-files/fresh_install.sql"
	docker exec -it surftimer-64t bash -c "mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) surftimer < /home/csgo/server/csgo/SurfZones/Zones/REPLACE_ALL_maptier.sql"
	docker exec -it surftimer-64t bash -c "mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) surftimer < /home/csgo/server/csgo/SurfZones/Zones/REPLACE_ALL_spawnlocations.sql"
	docker exec -it surftimer-64t bash -c "mysql -u root -h 127.0.0.1 --password=$(DB_PASSWORD) surftimer < /home/csgo/server/csgo/SurfZones/Zones/REPLACE_ALL_zones.sql"
	docker-compose down

bootstrap: build plugin/bootstrap db/bootstrap

serve-64t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I | cut -d' ' -f 1) \
	CSGO_GSLT=$(CSGO_GSLT) \
		docker-compose up -d surftimer-64t
	docker-compose logs -f

serve-100t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I | cut -d' ' -f 1) \
	CSGO_GSLT=$(CSGO_GSLT) \
		docker-compose up -d surftimer-100t
	docker-compose logs -f

.PHONY: build bootstrap plugin/bootstrap db/bootstrap serve-64t serve-100t
