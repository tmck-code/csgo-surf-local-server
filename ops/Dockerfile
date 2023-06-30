FROM cm2network/csgo:sourcemod

USER root

RUN apt update \
    && apt install -y git unzip

WORKDIR /home/surf

ADD ops ./ops
