# Preseed Action

The `preseed` action defines the contents of the `<profile>.preseed` file. This
file will contain the preconfiguration for the Debian installer. The `preseed`
action takes in a `jinja` template of the preseed file, in which chosen
configuration parameters are replaced with `jinja` variables. Finally, it
replaces the parameters with the provided substition variables.

!!! tip  
    Check out the Debian documentation on the [contents of the
    preconfiguration file](https://www.debian.org/releases/stable/amd64/apbs04.en.html) to learn more about the preseed file.

## Usage

Click on the :material-plus-circle: to learn more about the action's options.

```yaml title="Preseed Action"
{% set username=username or "user" -%}
{% set user_fullname=user_fullname or "User" -%}

actions:
  - action: preseed
    description: Basic preseed file for minimum Debian system with EFI boot #(1)!
    preconf: preseeds/base-preseed.txt # (2)!
    variables: # (3)! 
      user_fullname: {{user_fullname}}
      username: {{username}}
```

1. [**Optional**] Description, for documentation purposes
2. [**Required**] Relative link to the preseed template file
3. [**Optional**] Substition variables

## Implementation

### ::: simple_cdd_yaml.actions.PreseedAction
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
