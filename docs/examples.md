# Examples

Examples of working recipes can be found in
[simple-cdd-yam-recipes](https://github.com/swvanbuuren/simple-cdd-yaml-recipes).

## Example recipe `base` 

The simplest recipe that
[simple-cdd-yam-recipes](https://github.com/swvanbuuren/simple-cdd-yaml-recipes)
features is the recipe
[`base`](https://github.com/swvanbuuren/simple-cdd-yaml-recipes/blob/master/recipes/base.yaml),
which is shown below.

The recipe consists of:

- A series of variables with default values, which can be overridded when
  including this recipe in another recipe. Variables are used throughout the recipe using the `jinja2` notation `{{variable}}`.
- Profile name definition.
- A series of actions:
    - `recipe` action. Include another recipe, where some variables are being
      overridden.
    - `conf` action: Set simple-CDD variables and environment variables.
    - `preseed` action: The Debian-CD configuration is controlled via preseed.
      files. Here, a template is used in which variables are substituted.
    - `apt` action: Install Debian packages.
    - `run` action (`script`): Runs a script. Note that variables in the script
      also might get substituted.
    - `run` action (`command`): Runs a command.
    - `overlay` action: Deploys the contents of a give directory onto the
      system. This can be done by `root` (default) or by a given user.
- Also note that it's possible to include more complex behavior using `jinja2`,
  such as if-statements as shown in this example.

```yaml title="base.yaml"
--8<-- "https://raw.githubusercontent.com/swvanbuuren/simple-cdd-yaml-recipes/master/recipes/base.yaml"
```
