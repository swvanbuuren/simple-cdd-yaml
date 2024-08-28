# Installation

It is recommended to install Simple-CDD-YAML into a dedicated environment (e.g.
[virtaulenv](https://github.com/pypa/virtualenv)). After the environment has been activated, it can simply installed using `pip`:

```bash
pip install simple-cdd-yaml
``` 

Alternatively, Simple-CDD-YAML can be installed from source:

```bash
git clone https://github.com/swvanbuuren/simple-cdd-yaml.git
cd simple-cdd-yaml
pip install .
```

## Usage

Now that Simple-CDD-YAML is installed, the command `simple-cdd-yaml` should be
available in your virtual python environment. You can test it out, by querying
the help:

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
