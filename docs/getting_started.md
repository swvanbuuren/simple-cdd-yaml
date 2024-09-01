# Getting started

This page will guide you through the process of installing Simple-CDD-YAML and
generating a Simple-CDD profile from a YAML recipe.

## Installation

Install Simple-CDD-YAML according to the [installation
instructions](installation.md).

## Usage

Now that Simple-CDD-YAML is installed, the command `simple-cdd-yaml` should be
available. Make sure the appropriate environment (in which `simple-cdd-yaml` is
installed) has been activated prior to issuing this command.  You can test it
out, by querying the help:

```bash
simple-cdd-yaml --help
```

This should result in the following output:

```console
usage: simple-cdd-yaml [-h] --recipe RECIPE [--profile PROFILE] 
       [--output OUTPUT] [--input INPUT] [--debos] 
       [--debos-output DEBOS_OUTPUT] [--vars key1=value1,key2=value2,...]

Generate simple-cdd profiles using YAML input

options:
  -h, --help            show this help message and exit
  --recipe RECIPE       set the config yaml file
  --profile PROFILE     profile name
  --output OUTPUT       profile output directory (default: .)
  --input INPUT         recipe/action working directory (default: .)
  --debos               if provided, try to generate a debos recipe instead
  --debos-output DEBOS_OUTPUT
                        debos recipe output directory (default: ./debos)
  --vars key1=value1,key2=value2,...
                        override root recipe variables
```

## Building a Simple-CDD profile

In order to build a profile from a given recipe file `<recipe-name>.yaml`,
located in the subdirectory `recipe`, issue:

```bash
simple-cdd-yaml --recipe recipe/<recipe-name>.yaml
``` 

Make sure the appropriate environment (in which `simple-cdd-yaml` is installed)
has been activated prior to issuing this command. Alternatively, you can
prepend the environment activation (here called `<simple-cdd-yaml-venv>`):

```bash
( . ~/.venv/<simple-cdd-yaml-venv>/bin/activate && \
    simple-cdd-yaml --recipe recipe/<recipe-name>.yaml )
```

Note that the commands are wrapped in parentheses `( ... )` in order to assure
that the commands run in an isolated shell.

## Results

After a successful build, a `profiles` directory should become visible that
contains the Simple-CDD outputs, all named after profile name `<profile>`, but with different extensions. These include:

- `<profile>.preseed`
- `<profile>.packages`
- `<profile>.postinst`
- `<profile>.conf`
- `<profile>.extra`
- `<profile>.downloads`

The last file `<profile>.extra` contains references to additional files that are
included into the profile. These are located in the directory `extra`. Finally,
also a `debos` directory might appear, if you enabled the `debos` output option
during profile build and included a corresponding action into the recipe.

Visit the [Simple-CDD repository](https://salsa.debian.org/debian/simple-cdd) or
[Howto](https://wiki.debian.org/Simple-CDD/Howto) to learn more about the
contents of profile files and how to build an images from them using [Simple-CDD](https://wiki.debian.org/Simple-CDD).
