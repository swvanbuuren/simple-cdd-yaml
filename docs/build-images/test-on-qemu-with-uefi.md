# Test on Qemu with UEFI

The exemplary [desktop
recipe](https://github.com/swvanbuuren/simple-cdd-yaml-recipes/blob/master/recipes/desktop.yaml)
creates a Simple-CDD profile for an UEFI capable desktop system. While
Simple-CDD [offers a qemu
option](https://salsa.debian.org/debian/simple-cdd/-/blob/master/README?plain=1#L49)
to test the installation of a CD or DVD created with Simple-CDD, it does not
support UEFI. The following shows how to boot a Qemu with UEFI support in order
to test the installation in EFI mode. 

## Prerequisites

The following setup is meant for Debian systems and was tested on Debian Bullseye.

## Preparations

In order to be able to build an ISO image, first install the required packages
for Simple-CDD:
```
sudo apt install simple-cdd xorriso
```
Then build an image from the desktop profile:
```
build-simple-cdd --profiles desktop
```
This should produce an ISO file in the folder `images`.

Please refer to the [Simple-CDD website](https://salsa.debian.org/debian/simple-cdd) and the
corresponding [Debian Wiki Simple-CDD Howto page](https://wiki.debian.org/Simple-CDD/Howto)
for more information.

## Setup Qemu

To test the installation image Qemu can be used. Install the required packages
using:
```
sudo apt install qemu-utils qemu-system-x86 ovmf qemu-system-gui
```
The package `ovmf` is required for UEFI support.

Now create some images for testing, e.g.
```
qemu-img create -f qcow2 disk.qcow2 10G
qemu-img create -f qcow2 second_disk.qcow2 10G
```
Create a bash script stored as `image_run` with the following contents (don't
forget to make it executable using `chmod +x image_run`)

```bash
#!/bin/bash
if [ $# -eq 0 ] ; then
    cdrom="-boot c"
else
    cdrom="-boot d -drive media=cdrom,readonly=on,file=${1}"
fi
qemu-system-x86_64 \
    -m 2048 \
    -enable-kvm \
    -cpu host \
    ${cdrom} \
    -drive if=pflash,format=raw,readonly=on,file=/usr/share/ovmf/OVMF.fd \
    -drive format=qcow2,file=disk.qcow2 \
    -drive format=qcow2,file=second_disk.qcow2
```

## Testing using Qemu

Test the Simple-CDD installation by issuing (replace `<simple-cdd-iso>` with the
iso file as created by Simple-CDD):
```
./image_run images/<simple-cdd-iso>
```
After the installation has been completed succesfully, test out the installed
desktop system using 

```
./image_run
```
