# Simple-CDD-YAML

Preprocesser for [Simple-CDD](https://salsa.debian.org/debian/simple-cdd) using
YAML input files (so-called recipes), as inspired by
[debos](https://github.com/go-debos/debos).

## Introduction

Simple-CDD-YAML uses so-called recipes in YAML format with which the profile
files required Simple-CDD are generated. A recipe consists of actions, that
generate or append files in the Simple-CDD profile. Simple-CDD-YAML features the
following actions:

- `recipe` action: embed another recipe
- `conf` action: compose a `*.conf` file by supplying (environment) variables
- `preseed` action: define a preseed file
- `apt` action: add packages
- `run` action: add a command or script (to `*.postinst`)
- `overlay` action: add an overlay. An overlay is a file structure that is
  compressed into one single file and automatically added to `*.extra`.  
  A corresponding command to decompress the overly is added `*.postinst`
- `extra` action: add extra file
- `downloads` action: add extra packages
- `debos` action: [only in debos mode] add pre- and post-action to debos recipe
  output

Some of the actions support substitutions using
[jinja](https://palletsprojects.com/p/jinja/) notation, making it easier to
reuse scripts, preseeds and recipes. By defining variables with default values
at the top of a recipe it becomes easy to reuse and nest recipes.

A few actions also support different roles: by default a script is run or an
overlay is deployed as root, but you can also specify to have this done by a
certain user.

Please refer to the [documentation](#documentation) for more information.

## Installation

Simple-CDD-YAML can be installed using `pip`:
```
pip install git+https://github.com/swvanbuuren/simple-cdd-yaml.git
```

## Usage

After installation use the command `simple-cdd-yaml` to create Simple-CDD
profiles from YAML files. Issue `simple-cdd-yaml --help` to get help.

## Examples

Refer to
[simple-cdd-yaml-recipes](https://github.com/swvanbuuren/simple-cdd-yaml-recipes)
for example recipes.

## Documentation

Check out [the documentation](https://swvanbuuren.github.io/simple-cdd-yaml/) to
get started, find more background information and query the API Reference.

## License

An MIT style license applies for Simple-CDD-YAML, see the [LICENSE](LICENSE)
file for more details.
