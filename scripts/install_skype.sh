#!/bin/sh
curl -sS https://repo.skype.com/data/SKYPE-GPG-KEY \
     | gpg --dearmor --yes -o /etc/apt/trusted.gpg.d/skype.gpg
echo "deb https://repo.skype.com/deb stable main" \
    | tee /etc/apt/sources.list.d/skype.list
apt-get update
apt-get install --no-install-recommends -y skypeforlinux
