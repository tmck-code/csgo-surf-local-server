build:
	docker build -f ops/Dockerfile -t csgo-surf .

bootstrap:
	docker run -it -v $(PWD):/home/surf csgo-surf ./ops/bootstrap.sh

serve-64t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I) \
	CSGO_GSLT=$CSGO_GSLT \
		docker-compose up server-64t

serve-100t:
	SRCDS_NET_PUBLIC_ADDRESS=$(shell hostname -I) \
	CSGO_GSLT=$CSGO_GSLT \
		docker-compose up server-100t

.PHONY: build bootstrap serve-64t serve-100t
