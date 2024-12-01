# Simple-CDD-YAML

Preprocessor for [Simple-CDD](https://wiki.debian.org/Simple-CDD) using
YAML input files (so-called recipes), as inspired by
[debos](https://github.com/go-debos/debos).

Simple-CDD is a tool for creating customized debian-installer CDs.

## Introduction

Simple-CDD-YAML uses YAML recipes to generate the profile files required by
Simple-CDD. A recipe consists of actions, that generate or append files in the
Simple-CDD profile. Simple-CDD-YAML features the following actions (for an
exemplary profile called `<profile>`):

- `recipe` action: embed another recipe
- `conf` action: compose a `<profile>.conf` file by supplying (environment)
  variables
- `preseed` action: define a preseed file
- `apt` action: add packages
- `run` action: add a command or script (to `<profile>.postinst`)
- `overlay` action: add an overlay (an overlay is a file structure that is
  compressed into one single file and automatically added to the file
  `<profile>.extra`. A corresponding command to decompress the overlay is added
  to `<profile>.postinst`)
- `extra` action: add extra file
- `downloads` action: add extra packages
- `debos` action: [only in debos mode] add pre- and post-action to debos recipe
  output

Some of the actions support substitutions using
[jinja](https://palletsprojects.com/p/jinja/) notation, making it easier to
reuse scripts, preseeds and recipes. By defining variables with default values
at the top of a recipe it becomes easy to reuse and nest recipes.

A few actions also support different roles: by default scripts are executed and
overlays are deployed as root, but you can also specify to have this done by a
given user.

Please refer to the [documentation on
actions](https://swvanbuuren.github.io/simple-cdd-yaml/actions/) for detailed
documentation for each action.

## Installation

Simple-CDD-YAML can be directly installed from [PyPi](https://pypi.org) using
`pip`:

```bash
pip install simple-cdd-yaml
```

Detailed instructions are found in the documentation's [installation
section](https://swvanbuuren.github.io/simple-cdd-yaml/installation/).

## Usage

After installation use the command `simple-cdd-yaml` to create Simple-CDD
profiles from YAML files. Issue `simple-cdd-yaml --help` to get help.

Detailed usage instructions are found in the [getting
started](https://swvanbuuren.github.io/simple-cdd-yaml/getting_started/) guide.

## Examples

 Refer to the documentation's [examples
 page](https://swvanbuuren.github.io/simple-cdd-yaml/examples/) for a detailed
 recipe explanation. The repository
 [simple-cdd-yaml-recipes](https://github.com/swvanbuuren/simple-cdd-yaml-recipes)
 contains more example recipes.

## Documentation

Check out the [documentation](https://swvanbuuren.github.io/simple-cdd-yaml/) to
get started, find more background information and query the code reference.

## Pre-commit hooks

This repository comes with pre-commit hooks, which are stored in
[`.hooks`](.hooks). To enable the hooks issue:

```bash
git config --local core.hooksPath .hooks/
```

## License

An MIT style license applies for Simple-CDD-YAML, see the [LICENSE](LICENSE)
file for more details.
