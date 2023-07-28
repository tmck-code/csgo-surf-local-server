build:
	docker build -f ops/Dockerfile -t csgo-surf .

bootstrap:
	docker run -it -v $(PWD):/home/surf csgo-surf ./ops/bootstrap.sh

.PHONY: build bootstrap
