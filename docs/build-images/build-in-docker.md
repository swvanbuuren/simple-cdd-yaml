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
RUN apt-get -y install --install-recommends simple-cdd xorriso gpg distro-info-data

RUN sed -i 's/if a == "amd64" and "i386" not in self.env.get("ARCHES"):/if False and a == "amd64" and "i386" not in self.env.get("ARCHES"):/' /usr/share/simple-cdd/build-simple-cdd  
#(1)!

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user
```

1. When building with Simple-CDD v0.6.9, this hack is necessary to disable the
   enforcement of installing the i386 installer for amd64 builds. This will
   fail, because this installer was removed from Trixie.

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
