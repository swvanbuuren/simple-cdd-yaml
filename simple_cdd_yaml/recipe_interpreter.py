""" YAML recipe interpreter module """

import pathlib as pl
import shutil
import stat
import jinja2
from simple_cdd_yaml import actions
import simple_cdd_yaml.yaml_tools as yt


POSTINST_TEMPLATE_STR = \
"""#!/bin/sh

# Find and set variables
PROFILE={{profile}}
# Mount cdrom and set Simple-CDD EXTRAS location
mkdir -p /mnt/cdrom
mount -o ro /dev/sr0 /mnt/cdrom
SCDD_EXTRAS=""
for mounted in /media/*/ /cdrom/ /mnt/cdrom/ ; do
    candidate=$mounted"simple-cdd"
    if [ -d "$candidate" ] ; then SCDD_EXTRAS="$candidate"; break; fi
done
echo "SCDD_EXTRAS=$SCDD_EXTRAS"

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
        self.debos = args.debos
        self.debos_output_dir = pl.Path(args.debos_output) / self.profile
        self.recipe_vars = args.recipe_vars
        self.recipe_action = actions.RecipeAction(vars(args))

    def _recipe_props(self):
        """ Get root recipe properties """
        return {
            'action': 'recipe',
            'description': f'Load {self.profile} recipe',
            'recipe': self.recipe_file,
            'variables': dict(self.recipe_vars, debos=self.debos),
        }

    def _recipe_closing(self):
        """ Print out recipe closing statement """
        print(''.center(70, '='))
        print(' Recipe done.')

    def find_profile_name(self, args):
        """ Try to find profile name """
        full_yaml = yt.load_yaml(self.recipe_file)
        if profile := full_yaml.get('profile'):
            args.profile = profile
            return profile
        if args.profile:
            return args.profile
        raise ProfileException('Profile not defined or found in recipe file!')

    def generate_profile(self):
        """ Generate simple-cdd profile output """
        self._clear_profile()
        self.recipe_action.execute(self._recipe_props())
        self._recipe_closing()

    def generate_debos_recipe(self):
        """ Generate and obtain results dict and output to debos yaml recipe """
        self._clear_debos_recipe()
        output_file = self.debos_output_dir  / (self.profile + '.yaml')
        self.recipe_action.execute(self._recipe_props())
        result_dict = self.recipe_action.get_result()
        debos_recipe = {
            'architecture': result_dict['architecture'], 
            'actions': [],
        }
        for action_list in ('pre-actions', 'actions', 'post-actions'):
            debos_recipe['actions'] += result_dict[action_list]
        if result_dict.get('chroot_default'):
            for item in debos_recipe['actions']:
                if item.get('action') == 'run' and 'chroot' not in item and 'postprocess' not in item:
                    item['chroot'] = True
        yt.save_yaml(output_file, debos_recipe)
        script_dir = self.debos_output_dir / 'scripts'
        for file in script_dir.iterdir():
            self._make_executable(file)
        self._recipe_closing()

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
        output_file = self.output_dir / directory / filename
        with open(output_file, mode='a', encoding='utf-8') as file:
            file.write(string)

    def _clear_debos_recipe(self):
        debos_dir = self.debos_output_dir
        if debos_dir.is_dir():
            shutil.rmtree(debos_dir)
        self._create_dir(debos_dir)
        self._create_dir(self.debos_output_dir / 'scripts')
        self._create_dir(self.debos_output_dir / 'overlays')

    @staticmethod
    def _create_dir(pathlib_dir):
        """ Creates a directory, even if it already exists """
        pathlib_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _make_executable(file):
        """ Adds executable permissions to file """
        file.chmod(file.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
