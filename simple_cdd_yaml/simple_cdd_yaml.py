""" Simple-cdd YAML recipe interpreter """

import argparse
import simple_cdd_yaml.recipe_interpreter as interp


def main():
    """ Command line interface for Simple-CDD-Yaml """
    parser = argparse.ArgumentParser(description='Generate simple-cdd profiles using YAML input')
    parser.add_argument('--recipe', type=str, required=True,
                        help='set the config yaml file')
    parser.add_argument('--profile', type=str, default=None,
                        help='profile name')
    parser.add_argument('--dist', type=str, default='bullseye',
                        help='Debian distribution (default: bullseye)')
    parser.add_argument('--output', type=str, default='.',
                        help='Profile output directory')
    parser.add_argument('--input', type=str, default='.',
                        help='Recipe/action working directory')
    parser.add_argument('--debos', default=False, action='store_true',
                        help='If provided, try to generate a debos recipe')
    parser.add_argument('--debos-output', type=str, default='./debos',
                        help='Debos recipe output directory')
    try:
        arguments = parser.parse_args()
        if arguments.debos:
            interp.YamlRecipeInterpreter(arguments).generate_debos_recipe()
        else:
            interp.YamlRecipeInterpreter(arguments).generate_profile()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
