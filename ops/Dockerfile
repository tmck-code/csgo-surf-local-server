FROM cm2network/csgo:sourcemod

USER root

RUN apt update \
    && apt install -y git unzip

ENV SURFTIMER_ZIP https://github.com/surftimer/SurfTimer/releases/download/1.1.4/SurfTimer.1.1.4.914.6a563cd.SM1.11.zip
RUN cd /tmp \
    && curl -L $SURFTIMER_ZIP -o surftimer.zip
    # && unzip surftimer.zip -d /home/steam/csgo-dedicated/csgo/ \
    # && rm surftimer.zip

WORKDIR /home/surf

ADD ops ./ops
