#!/bin/bash

set -euxo pipefail

PLATFORM=linux64

if ! test -e /usr/bin/google-chrome; then
  # credit: https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/
  sudo apt install -y curl unzip xvfb libxi6 libgconf-2-4
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo apt install ./google-chrome-stable_current_amd64.deb
  google-chrome --version
fi

# this is a handy API that's directly recommended by the official chromedriver
# download page (https://chromedriver.chromium.org/downloads)
chrome_versions=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json)
# e.g. https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.69/linux64/chromedriver-linux64.zip
url_for_version=$(
  echo $chrome_versions \
    | jq -r ".versions[]
      | select( .version == \"$(/usr/bin/google-chrome --version | cut -d' ' -f3)\" )
      | .downloads.chromedriver[]
      | select( .platform == \"$PLATFORM\" )
      | .url"
)

if [ -n "${url_for_version:-}" ]; then
  rm -rf "chromedriver-${PLATFORM}*"
  wget $url_for_version
  unzip chromedriver-linux64.zip
fi

