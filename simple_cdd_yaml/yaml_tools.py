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


class LevelWhiteLineDumper(yaml.SafeDumper):
    """ Adds white lines on below a given yaml object level """
    level = 1

    @classmethod
    def set_level(cls, level):
        """ Level below which white lines are included  """
        cls.level = level
        return cls

    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < self.level + 1:
            super().write_line_break()


def save_yaml(filepath, yaml_dict):
    """ Store dictionary as yaml file """
    with open(filepath, mode='w+', encoding="utf-8") as file:
        yaml.dump(yaml_dict, file, Dumper=LevelWhiteLineDumper.set_level(2),
                  allow_unicode=True, width=4096, sort_keys=False)
