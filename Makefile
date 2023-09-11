build:
	docker build -f ops/Dockerfile -t csgo-surf .

bootstrap: build
	docker create --name csgo-surf csgo-surf
	docker cp csgo-surf:/home/steam/csgo-dedicated/csgo ./data
	docker rm -f csgo-surf

serve-64t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I | cut -d' ' -f 1) \
	CSGO_GSLT=$(CSGO_GSLT) \
		docker-compose up surftimer-64t

serve-100t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I | cut -d' ' -f 1) \
	CSGO_GSLT=$(CSGO_GSLT) \
		docker-compose up surftimer-100t

.PHONY: build bootstrap serve-64t serve-100t bootstrap
