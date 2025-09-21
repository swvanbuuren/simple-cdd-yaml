# Build in Docker

To make sure that the host system configuration does not interfere with a
simple-CDD build, it's useful to build the image inside a docker container. The
following lists instructions to setup such a docker image.

## Install and configure docker

First, install and configure docker. Please refer to the script
[setup_docker.sh](https://github.com/swvanbuuren/simple-cdd-yaml-recipes/blob/master/scripts/setup_docker.sh)
on how to do this.

## Dockerfile

First create a file called `Dockerfile` with the contents below. Replace
`<dist>` with the Debian version for which you'd like to build your image, e.g.
`buster`, `bullseye` or `bookworm`:

```Dockerfile
FROM debian:<dist>-slim

RUN apt-get update
RUN apt-get -y install --install-recommends xorriso gpg distro-info-data wget

RUN apt-get -y install --install-recommends xorriso gpg distro-info-data wget
RUN wget https://deb.debian.org/debian/pool/main/s/simple-cdd/simple-cdd_0.6.10_all.deb
RUN wget https://deb.debian.org/debian/pool/main/s/simple-cdd/python3-simple-cdd_0.6.10_all.deb
RUN apt-get -y install ./simple-cdd_0.6.10_all.deb ./python3-simple-cdd_0.6.10_all.deb
#(1)!

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user
```

1. Simple-CDD v0.6.9 contains a bug, which has been resolved in v0.6.10.
   Unfortunately, the Trixie repositories still contain v0.6.9. Therefore, we install the newer version manually.

## Build docker image

Build the docker image with the following command (again replace `<dist>`):
```bash
docker build -t <dist>-simple-cdd .
```

## Call simple-cdd inside docker

For repeated build attempts, it makes sense to wrap the dockerized simple-CDD
call into a bash script e.g. called `docker_simple_cdd` (don't forget to replace
`<dist>` and make the script executable using `chmod +x docker_simple_cdd`):
```bash
#!/bin/bash
ARGS="$@"
docker run -it --mount "type=bind,source=$(pwd),destination=/home/user" <dist>-simple-cdd /bin/sh -c "simple-cdd $ARGS"
```

Now you can build an image e.g. from the desktop profile by issuing:

```bash
./docker_simple_cdd --profiles desktop
```
