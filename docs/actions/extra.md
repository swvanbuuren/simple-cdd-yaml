# ExtraAction

The `extra` action includes extra files for the installation. Files are
registered in `<profile>.extra` and copied to the `extra` directory.

## Usage

Click on the :material-plus-circle: to learn more about the action's options.

```yaml title="Extra Action"
actions:
  - action: extra
    description: Extra files #(1)!
    files: # (2)! 
      - path/to/file
      - path/to/another-file
```

1. [**Optional**] Description, for documentation purposes
2. [**Required**] List of file paths

## Implementation

### ::: simple_cdd_yaml.actions.ExtraAction
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
