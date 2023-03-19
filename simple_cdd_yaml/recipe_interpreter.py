""" YAML recipe interpreter module """

import pathlib as pl
import stat
import jinja2
from simple_cdd_yaml import actions
from simple_cdd_yaml.yaml_loader import load_yaml


POSTINST_TEMPLATE_STR = \
"""#!/bin/sh

# Find and set variables
PROFILE={{profile}}
for mounted in /media/*/ ; do
    candidate=$mounted"simple-cdd"
    if [ -d "$candidate" ] ; then SCDD_EXTRAS="$candidate"; break; fi
done

"""


class ProfileException(Exception):
    """ Raised when profile has not been defined """


class YamlRecipeInterpreter():
    """ Yaml recipe interpreter for simple-cdd """
    def __init__(self, args):
        self.recipe_file = args.recipe
        self.profile = self.find_profile_name(args)
        self.output_dir = pl.Path(args.output)
        self.postinst_template = jinja2.Template(POSTINST_TEMPLATE_STR)
        self.recipe_action = actions.RecipeAction(args)

    def find_profile_name(self, args):
        """ Try to find profile name """
        full_yaml = load_yaml(self.recipe_file)
        if profile := full_yaml.get('profile'):
            args.profile = profile
            return profile
        if args.profile:
            return args.profile
        raise ProfileException('Profile not defined or found in recipe file!')

    def generate_profile(self):
        """ Generate simple-cdd profile output """
        self._clear_profile()
        props = {
            'action': 'recipe',
            'description': f'Load {self.profile} recipe',
            'recipe': self.recipe_file,
            'substitutions': None,
        }

        self.recipe_action.execute(props)
        print(''.center(70, '='))
        print(' Recipe done.')

    @staticmethod
    def _make_executable(file):
        """ Adds executable permissions to file """
        file.chmod(file.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def _clear_profile(self):
        """ Remove any pre-existing profile files in output directories """
        profiles_dir = self.output_dir / 'profiles'
        profiles_dir.mkdir(parents=True, exist_ok=True)
        wildcard = self.profile + '.*'
        for file in profiles_dir.glob(wildcard):
            file.unlink()
        extra_dir = self.output_dir / 'extra'
        extra_dir.mkdir(parents=True, exist_ok=True)
        for file in extra_dir.glob(wildcard):
            file.unlink()
        postinst_str = self.postinst_template.render(profile=self.profile)
        self._write_action(postinst_str, 'postinst')
        self._make_executable(profiles_dir / (self.profile + '.postinst'))

    def _write_action(self, string, extension, directory='profiles'):
        """ Append string to profile file """
        filename = self.profile + '.' + extension
        outpout_file = self.output_dir / directory / filename
        with open(outpout_file, mode='a', encoding='utf-8') as file:
            file.write(string)
