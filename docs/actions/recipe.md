# Recipe Action

The `recipe` action embeds another `YAML` recipe. This action offers the
possibility to substitute variables in the recipe that will be embedded.

## Usage

Click on the :material-plus-circle: to learn more about the action's options.

```yaml title="Recipe Action"
{% set username=username or "user" -%}

actions:
  - action: recipe
    description: Recipe that will be embedded # (1)!
    recipe: recipes/recipe.yaml # (2)!
    working_dir: upstream # (3)! 
    variables: # (4)! 
      username: {{username}}
```

1. [**Optional**] Recipe description, for documentation purposes
2. [**Required**] Relative link to the recipe's `YAML` file
3. [**Optional**] Alternative working directory. This is required to avoid
   breaking relative links, when embedding a recipe from another location.
4. [**Optional**] Substition variables

## Implementation

### ::: simple_cdd_yaml.actions.RecipeAction
    options:
      members: false
      show_root_heading: true
      show_root_full_path: false
