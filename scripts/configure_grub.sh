#!/bin/sh
grub2default=/etc/default/grub
if [ -f "$grub2default" ]; then
    # remove keywords from CMDLINE_LINUX_DEFAULT
    for keyword in "quiet splash"; do
	sed -i "/GRUB_CMDLINE_LINUX_DEFAULT/s/$keyword//g" $grub2default
    done
    # set timeout to zero
    sed -i '/GRUB_TIMEOUT/c\GRUB_TIMEOUT=0' $grub2default
    # ensure the updates go live
    update-grub
fi
