# Run Action

The `run` action actions allows to either run a script or a command. The
corresponding code is automatically appended to `<profile>.postinst`. This
script or command is executed by root by default. However, it's also possible to
have another user execute the command. The script may contain `jinja` variables,
that are substituted using provided substition variables.

!!! info  
    It's not possible to combine a script and command in one single `run` action. In other words, the `command` and `script` keywords are mutually exclusive.

## Usage

Click on the :material-plus-circle: to learn more about the action's options.

```yaml title="Run Action (command)"
{% set username=username or "user" -%}

actions:
  - action: run
    description: Add {{username}} to sudoers #(1)!
    variables: #(2)!
      username: {{username}}
    script: scripts/add_sudoer.sh  #(3)!
```

1. [**Optional**] Description, for documentation purposes
2. [**Optional**] Substition variables
3. [**Required**] Relative link to the script file. Mutually exclusive with the
   `command` keyword.


```yaml title="Run Action (script)"
  - action: run
    description: Make sure debian UEFI file is registered as boot entry #(1)!
    user: {{username}} # (2)!
    command: | # (3)!
      grub-install --efi-directory /boot/efi --force-extra-removable --recheck
      && update-grub
```

1. [**Optional**] Description, for documentation purposes
2. [**Optional**] User that executes the command. If omitted, the command is
   executed by root.
3. [**Required**] The command to be executed. Mutually exclusive with the
   `script` keyword.


## Implementation

### ::: simple_cdd_yaml.actions.RunAction
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
