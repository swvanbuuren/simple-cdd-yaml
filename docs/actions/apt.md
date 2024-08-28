# Apt Action

The `apt` action defines the contents of `<profile>.packages` file, which
basically is a list of to be installed packages.

## Usage

Click on the :material-plus-circle: to learn more about the action's options.

```yaml title="Apt Action"
actions:
  - action: apt
    description: Base packages #(1)!
    packages: # (2)! 
      - adduser
      - apparmor
      - apt
```

1. [**Optional**] Description, for documentation purposes
2. [**Required**] List of packages


## Implementation

### ::: simple_cdd_yaml.actions.PreseedAction
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
