# Downloads Action

The `downloads` action includes additional packages to `<profile>.downloads`.
These packages aren't installed by default during the installation, but are
still included on the installation CD. This might be useful to include package
dependencies, which for some reason aren't deduced properly. The installer will
query these packages, whenever it encounters a missing package dependency.

## Usage

Click on the :material-plus-circle: to learn more about the action's options.

```yaml title="Downloads Action"
actions:
  - action: downloads
    description: Additional packages #(1)!
    packages: # (2)! 
      - usbutils
      - acpi
```

1. [**Optional**] Description, for documentation purposes
2. [**Required**] List of packages


## Implementation

### ::: simple_cdd_yaml.actions.DownloadsAction
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
