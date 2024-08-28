# Actions

This section documents each action type that Simple-CDD-YAML is able to use in
`YAML` recipes.

## Usage

Actions are listed under the root level `actions` keyword, which usually appears after the variables and profile name definition:

```yaml
{% set profile=profile or "base" -%} # (1)!

profile: {{profile}} # (2)!

actions:
  action: recipe
    description: ...
```

1. Note the value `profile or "base"`. This assigns the default value `base` to
   the variable `profile`. When defining a variable, it's recommended to set a
   default value.
2. Here, the value of the variable `profile` is substituted as profile name.

## Implementation

All actions inherit from the `Action` class.

### ::: simple_cdd_yaml.actions.Action
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
