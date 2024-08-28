# Conf Action

The `conf` action defines the contents of the `<profile>.conf` file. This file
contains normal variables and environment variables.

!!! tip 

    Have a look at the [source code of Simple-CDD on
    variables](https://salsa.debian.org/debian/simple-cdd/-/blob/master/simple_cdd/variables.py),
    to see which variables and environment variables are supported.

### Usage

Click on the :material-plus-circle: to learn more about the action's options.

```yaml title="Conf Action"
{% set profile=profile or "base" -%}
{% set mirror_components=mirror_components or "main" -%}
{% set disk_type=disk_type or "DVD" -%}
{% set dist=dist or "bookworm" -%}

  - action: conf
    description: Simple-CDD configuration settings # (1)!
    variables: # (2)!
      profiles: {{profile}}
      auto_profiles: {{profile}}
      mirror_components: {{mirror_components}}
    env_variables: # (3)!
      DISKTYPE: {{disk_type}}
      CODENAME: {{dist}}
```

1. [**Optional**] Description, for documentation purposes
2. [**Optional**] Variable definitions
3. [**Optional**] Environment variable definitions

## Implementation

### ::: simple_cdd_yaml.actions.ConfAction
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
