""" Simple-cdd YAML recipe interpreter """

import argparse
import simple_cdd_yaml.recipe_interpreter as interp


class KeyValueParseAction(argparse.Action):
    """ Parse comma separated key=value pairs """

    def __call__(self, parser, namespace, values, option_string=None):
        value_dict = {}
        for item in values.split(','):
            key, value = item.split('=')
            value_dict[key] = value
        setattr(namespace, self.dest, value_dict)


def main():
    """ Command line interface for Simple-CDD-Yaml """
    parser = argparse.ArgumentParser(description='Generate simple-cdd profiles using YAML input')
    parser.add_argument('--recipe', type=str, required=True,
                        help='set the config yaml file')
    parser.add_argument('--profile', type=str, default=None,
                        help='profile name')
    parser.add_argument('--output', type=str, default='.',
                        help='profile output directory (default: %(default)s)')
    parser.add_argument('--input', type=str, default='.',
                        help='recipe/action working directory (default: %(default)s)')
    parser.add_argument('--debos', default=False, action='store_true',
                        help='if provided, try to generate a debos recipe instead')
    parser.add_argument('--debos-output', type=str, default='./debos',
                        help='debos recipe output directory (default: %(default)s)')
    parser.add_argument('--vars', dest='recipe_vars', action=KeyValueParseAction,
                        default='', metavar='key1=value1,key2=value2,...',
                        help='override root recipe variables')
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
