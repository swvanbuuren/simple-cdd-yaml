""" YAML loader module """

import yaml
import jinja2


class NullUndefined(jinja2.Undefined):
    """ Jinja2 Undefined to parse jinja inside strings """
    def __getattr__(self, key):
        return ''


def load_yaml(file, substitutions=None):
    """ Load yaml file """
    if substitutions is None:
        substitutions = {}
    with open(file, mode="r", encoding="utf-8") as data:
        template = jinja2.Template(data.read(), undefined=NullUndefined)
    rendered = template.render(substitutions)
    return yaml.safe_load(rendered)


def save_yaml(filepath, yaml_dict):
    """ Store dictionary as yaml file """
    with open(filepath, mode='w+', encoding="utf-8") as file:
        yaml.dump(yaml_dict, file, allow_unicode=True)
