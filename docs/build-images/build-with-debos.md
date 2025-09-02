# Build with Debos

While the [test method with Qemu](test-on-qemu-with-uefi.md) tests all
installation image functionalities, it can be quite time consuming. An
alternative approach is to generate a [debos](https://github.com/go-debos/debos)
recipe from a Simple-CDD-YAML recipe and build and test its resulting image.
Building a debos image is generally much quicker and once built, does not
perform an installation process. Instead, the image can be tested straight away.

To generate a debos recipe, e.g. for the `desktop` recipe, issue the following:

```bash
simple-cdd-yaml --recipe recipes/desktop.yaml --debos
```

This will create debos recipe `desktop.yaml` along with all required scripts and
overlays in the `debos/desktop` directory.

To build the image, move into this directory and build using:
```
debos -m 8192MB --debug-shell desktop.yaml
```
Note that, depending on the recipe, the increased memory argument (`-m 8192MB`)
might not be required. 

After the image has been built successfully, it can be tested by starting it in a Qemu environment, e.g. using the following command.

```bash
qemu-system-x86_64 \
    -m 2048 \
    -enable-kvm \
    -cpu host \
    -drive if=pflash,format=raw,readonly=on,file=/usr/share/ovmf/OVMF.fd \
    -drive if=virtio,format=qcow2,cache=unsafe,file=debian-bookworm-amd64.qcow2
```
Please note that, depending on the recipe, the image name
`debian-bookworm-amd64.qcow2` might be different.
