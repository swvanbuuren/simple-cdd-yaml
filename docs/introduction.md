# Introduction

Simple-CDD-YAML uses YAML recipes to generate the profile files required by
Simple-CDD. A recipe consists of actions, that generate or append files in the
Simple-CDD profile.

## Actions

Simple-CDD-YAML features the following actions (for an
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

Visit the [Actions](actions/index.md) section to learn how to write actions and
see what they are capable of.

## Next steps

Refer to [getting started](getting_started.md) to install Simple-CDD-YAML,
create a profile from a YAML recipe and build an image using Simple-CDD.

Vist [code reference](reference/index.md) to learn more about the implementation and underlying code of Simple-CDD-YAML.
