#!/bin/bash

set -euxo pipefail

if ! test -e /usr/bin/google-chrome; then
  # credit: https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/
  sudo apt install -y curl unzip xvfb libxi6 libgconf-2-4
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo apt install ./google-chrome-stable_current_amd64.deb
  google-chrome --version
fi

CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/")
CHROME_DRIVER_VERSION=$(wget -qO- https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_MAJOR_VERSION} | sed 's/\r$//')
CHROME_DRIVER_URL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_DRIVER_VERSION/linux64/chromedriver-linux64.zip
echo $CHROME_DRIVER_URL
wget $CHROME_DRIVER_URL

unzip chromedriver-linux64.zip
