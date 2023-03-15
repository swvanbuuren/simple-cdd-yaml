#!/bin/bash
/usr/sbin/usermod -a -G sudo {{username}}
mkdir -p /etc/sudoers.d
echo "{{username}}	ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/{{username}}
