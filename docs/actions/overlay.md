# Overlay Action

The `overlay` action allows to overlay a file structure into the root file
system at the end of the installation. The corresponding command that takes care
of this is appended to `<profile>.postinst`. Corresponding archives that contain
the overlays are copied to the `extra` folder and are registered in
`<profile>.extra`. By default the overlay will be copied by root, but it's also
possible to have a user do this.

## Usage

Click on the :material-plus-circle: to learn more about the action's options.

```yaml title="Overlay Action"
{% set username=username or "user" -%}

actions:
  - action: overlay
    description: Bash settings for {{username}} #(1)!
    user: {{username}} #(2)!
    source: overlays/bash-settings #(3)!
    destination: /home/{{username}}/ #(4)!
```

1. [**Optional**] Description, for documentation purposes
2. [**Optional**] User that performs the overlay actions. If omitted root is
   used.
3. [**Required**] Relative link to overlay file structure
   `command` keyword.
 4. [**Optional**] Destination where the overlay file structure is copied to. If
    `destination` and `user` are omitted, `/` is used. If `destination` is omitted but `user` is provided, `/home/{user}` is used.

## Implementation

### ::: simple_cdd_yaml.actions.OverlayAction
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
