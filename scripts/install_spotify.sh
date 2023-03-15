#!/bin/sh
curl -sS https://download.spotify.com/debian/pubkey_7A3A762FAFD4A51F.gpg \
    | gpg --dearmor --yes -o /etc/apt/trusted.gpg.d/spotify.gpg
echo "deb http://repository.spotify.com stable non-free" \
    | tee /etc/apt/sources.list.d/spotify.list
apt-get update
apt-get install --no-install-recommends -y spotify-client
