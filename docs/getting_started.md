# Getting started

This page will code through to process of installing, generating a Simple-CDDp
rofile from a YAML recipe.

## Installation

First install Simple-CDD-YAML according to the [installation
instructions](installation.md).

## Building a Simple-CDD profile

In order to build a profile from a given recipe file `<recipe-name>.yaml`,
located in the subdirectory `recipe`, issue the following:

```bash
simple-cdd-yaml --recipe recipe/<recipe-name>.yaml
``` 

Make sure the  corresponding environment in which `simple-cdd-yaml` is installed
has been activated prior to issues this command. Alternatively, you can prepend
the command with a command to activate the environment (here called
`<simple-cdd-yaml-venv>`):

```bash
( . ~/.venv/<simple-cdd-yaml-venv>/bin/activate && \
    simple-cdd-yaml --recipe recipe/<recipe-name>.yaml )
```

Note that the commands are wrapped in parentheses `( ... )` to assure that the
command runs in an isolated shell.

## Results

After a successful build, a `profiles` directory should become visible that
contains the Simple-CDD outputs, all named after profile name `<profile>`, but with different extensions. These include:

- `<profile>.preseed`
- `<profile>.packages`
- `<profile>.postinst`
- `<profile>.conf`
- `<profile>.extra`

The last file `<profile>.extra` contains references to additional files that are
included into the profile. These are located in the directory `extra`. Finally,
also a `debos` directory might appear, if you enabled the `debos` output option
during profile build.

Visit the [Simple-CDD repository](https://salsa.debian.org/debian/simple-cdd) or
[Howto](https://wiki.debian.org/Simple-CDD/Howto) to learn more about the
contents of profile files and how to build an images from them using [Simple-CDD](https://wiki.debian.org/Simple-CDD).
