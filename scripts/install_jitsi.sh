#!/bin/sh
wget -qO - https://download.jitsi.org/jitsi-key.gpg.key \
    | gpg --dearmor --yes -o /etc/apt/trusted.gpg.d/jitsi.gpg
echo "deb https://download.jitsi.org stable/" \
    | tee /etc/apt/sources.list.d/jitsi-stable.list
apt-get update
apt-get install --no-install-recommends -y jitsi
