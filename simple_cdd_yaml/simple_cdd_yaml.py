""" Simple-cdd YAML recipe interpreter """

import argparse
import simple_cdd_yaml.recipe_interpreter as interp


def main():
    """ Command line interface for Simple-CDD-Yaml """
    parser = argparse.ArgumentParser(description='Generate simple-cdd profiles using YAML input')
    parser.add_argument('--recipe', type=str, required=True,
                        help='set the config yaml file')
    parser.add_argument('--profile', type=str, required=True,
                        help='profile name')
    parser.add_argument('--dist', type=str, default='bullseye',
                        help='Debian distribution (default: bullseye)')
    parser.add_argument('--output', type=str, default='.',
                        help='Profile output directory')
    try:
        arguments = parser.parse_args()
        interp.YamlRecipeInterpreter(arguments).generate_profile()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
