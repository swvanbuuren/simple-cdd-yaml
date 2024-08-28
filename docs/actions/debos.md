# Debos Action

The debos action is a special action that allows to generate a Debos version of
the Simple-CDD-YAML recipe. A Debos is only generated, when the user adds the
option `--debos` when issuing the `simple-cdd-yaml` command.

!!! info
    Only `overlay` and `run` actions are included in the debos recipe.

## Usage

Click on the :material-plus-circle: to learn more about the action's options.

```yaml title="Debos Action"
{% set architecture=architecture or "amd64" -%}

actions:
  - action: debos
    description: Debos recipe export settings and actions #(1)!
    architecture: {{ architecture }} #(2)!
    chroot_default: true #(3)!
    pre-actions: #(4)!
      ...

    post-actions: #(5)!
      ...
``` 

1. [**Optional**] Description, for documentation purposes
2. [**Required**] Architecture for which the Debos recipe should be generated
3. [**Optional**] Whether the actions should be executed in the target
   filesystem. This is option is only added to Simple-CDD-YAML actions, if the
   keyword `chroot` isn't set.
4. [**Required**] Debos specific actions that should be included *before* the
   Simple-CDD-YAML recipe.
5. [**Required**] Debos specific actions that should be included *after* the
   Simple-CDD-YAML recipe.


## Implementation

### ::: simple_cdd_yaml.actions.DebosAction
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
