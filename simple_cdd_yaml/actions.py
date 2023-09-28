""" Action handlers for Simple-cdd-yaml recipes """

import copy
import pathlib as pl
import tarfile
import re
import shutil
import textwrap
import jinja2
from simple_cdd_yaml.yaml_tools import load_yaml


PACKAGES_TEMPLATE_STR = \
"""
# {{description}}
apt-get update
apt-get install --no-install-recommends -y {{pkg_list}}

"""

OVERLAY_TEMPLATE_STR = \
"""
# {{description}}
tar -xf ${SCDD_EXTRAS}/{{overlay}} -C {{destination}}

"""


class ActionError(Exception):
    """ Raised when something goes wrong in an action """


class OwnerTarFilter:
    """ Parametrizable tar filer """
    def __init__(self, user, group=None):
        self.user = self.group = user
        if group:
            self.group = group

    def tar_filter(self, tarinfo : tarfile.TarInfo) -> tarfile.TarInfo:
        """ tar filter for modifying user/group name properties """
        tarinfo.uname = self.user
        tarinfo.gname = self.group
        return tarinfo

class Action:
    """ Abstract action base class """
    action_out = None

    def __init__(self, args_dict):
        self.profile = args_dict['profile']
        self.input_dir = pl.Path(args_dict['input'])
        self.output_dir = pl.Path(args_dict['output'])
        self.debos = args_dict['debos']
        self.debos_output_dir = pl.Path(args_dict['debos_output']) / self.profile
        self.result = []

    @staticmethod
    def _print(text, header=None, width=68):
        """ Print text wrapped """
        initial_indent = ' '
        if header:
            print(f' {header}')
            initial_indent = '  '
        wrapped_text = textwrap.wrap(
            text,
            width=width,
            initial_indent=initial_indent,
            subsequent_indent='  ',
            break_on_hyphens=False,
        )
        print('\n'.join(wrapped_text))

    def _action_inform(self, props):
        """ Inform on action start action status """
        if action_type := props.get('action'):
            print(f' {action_type} action '.upper().center(70, '='))
        if description := props.get('description'):
            self._print(f'Description: {description}')
        for src_file in ('recipe', 'preconf', 'source', 'command', 'script'):
            if src := props.get(src_file):
                self._print(f'{src_file.capitalize()}: {src}')

    def _read_substitute(self, filename, substitutions):
        """ Read string from file and perform jinja2 substitutions """
        input_file = self.input_dir / filename
        with open(input_file, mode='r', encoding='utf-8') as file:
            template = jinja2.Template(file.read())
        return template.render(substitutions)

    def _write_action(self, string, extension, directory='profiles',
                      no_duplicate=False):
        """ Append string to profile file """
        filename = self.profile + '.' + extension
        output_file = self.output_dir / directory / filename
        if no_duplicate and output_file.is_file():
            with open(output_file, mode='r', encoding='utf-8') as file:
                if string in file.read():
                    return
        with open(output_file, mode='a', encoding='utf-8') as file:
            file.write(string)

    def _perform_action(self, props):
        """ Perform the action specific tasks and return result """
        raise NotImplementedError('Action is an abstract base class!')

    def execute(self, props):
        """ Execute an action """
        self._action_inform(props)
        result = self._perform_action(props)
        if result:
            if not self.action_out:
                self.action_out = props['action']
            self._write_action(result, self.action_out)

    def append_result(self, new_result: dict):
        """ Append a new result to the result list """
        added_result = copy.deepcopy(new_result)
        self.result.append(added_result)


class ConfAction(Action):
    """ Conf action """
    def _perform_action(self, props):
        description = props.get('description', 'Conf settings')
        conf_str = f'# {description}\n'
        if variables := props.get('variables'):
            for var, value in variables.items():
                conf_str += f'{var}="{value}"\n'
        if env_variables := props.get('env_variables'):
            for var, value in env_variables.items():
                conf_str += f'export {var}="{value}"\n'
        if variables or env_variables:
            return conf_str


class PreseedAction(Action):
    """ Preseed action """
    def _perform_action(self, props):
        return self._read_substitute(props['preconf'],
                                     props.get('substitutions', {}))


class AptAction(Action):
    """ Apt action """
    action_out = 'packages'

    def __init__(self, args):
        super().__init__(args)
        self.packages_template = jinja2.Template(PACKAGES_TEMPLATE_STR)
        self.all_pkgs = set()

    def _perform_action(self, props):
        """ Process APT action """
        scripted = props.get('scripted', False)
        if packages := props.get('packages'):
            pkg_list = ' '.join(packages)
            self._print(pkg_list, header='Requested packages:')
            description = props.get('description', 'Install packages')
            if self.debos:
                self.append_result(props)
            if scripted:
                apt_install_script = self.packages_template.render(
                    description=description,
                    pkg_list=pkg_list)
                self._write_action(apt_install_script, extension='postinst')
                return None
            packages.insert(0, '# ' + description)
            return '\n'.join(packages) + '\n\n'


class OverlayAction(Action):
    """ Overlay action """
    def __init__(self, args):
        super().__init__(args)
        self.overlay_template = jinja2.Template(OVERLAY_TEMPLATE_STR)

    def _perform_action(self, props):
        description = props.get('description', 'Overlay')
        user = props.get('user')
        overlay_name = props['source'].replace('/', '.')
        source_dir = pl.PurePath(self.input_dir / props['source'])
        tar_filter = None
        destination = '/'
        if user:
            overlay_name += f'.{user}'
            tar_filter = OwnerTarFilter(user=user).tar_filter
            destination = f'/home/{user}/'
            if user == 'root':
                destination = '/root/'
        filename = f'{self.profile}.{overlay_name}.tar.gz'
        output_file = self.output_dir / 'extra' / filename
        with tarfile.open(output_file, "w:gz") as tar:
            tar.add(source_dir, arcname='', filter=tar_filter)
        extract_commands = self.overlay_template.render(
            description=description,
            overlay=filename,
            destination=destination,
        )
        self._write_action(f'extra/{filename}\n', extension='extra',
                           no_duplicate=True)
        self._write_action(extract_commands, extension='postinst')


class RunAction(Action):
    """ Run action """
    action_out = 'postinst'

    def _perform_action(self, props):
        if all(x in props for x in ['script', 'command']):
            raise ActionError('Too many keywords: script and command found!')
        if 'script' in props:
            return self.script(props)
        if 'command' in props:
            return self.command(props)
        raise ActionError('Missing script or command keyword!')

    def script(self, props):
        """ Shell commands to run a script """
        description = props.get('description', 'Run script')
        script = self._read_substitute(props['script'],
                                       props.get('substitutions', {}))
        script = re.sub(r'#!/bin/.*?sh\n', '', script)
        return f'\n# {description}\n{script}\n'

    def command(self, props):
        """ Shell code to run a command """
        description = props.get('description', 'Run command')
        template = jinja2.Template(props['command'])
        command = template.render(props.get('substitutions', {}))
        if user:= props.get('user'):
            command = f"su - {user} << 'EOF'\n{command}\nEOF"
        return f'\n# {description}\n{command}\n'


class ExtraAction(Action):
    """ Extra action """
    def _perform_action(self, props):
        description = props.get('description', 'Extra files')
        self._write_action(f'# {description}\n', extension='extra')
        extra_files = []
        for file in props['files']:
            src = pl.Path(file)
            dst = self.output_dir / 'extra' / src.name
            shutil.copyfile(src, dst)
            extra_files.append('extra/' + src.name)
        self._print(' '.join(extra_files), header='Extra files:')
        return '\n'.join(extra_files) + '\n'


class DownloadsAction(Action):
    """ Downloads action """
    def _perform_action(self, props):
        description = props.get('description', 'Additional packages')
        pkg_list = props['packages']
        self._print(' '.join(pkg_list), header='Extra packages:')
        downloads_pkg_list = '\n'.join(pkg_list)
        return f'# {description}\n{downloads_pkg_list}\n'


class DebosAction(Action):
    """ Debos action """
    def _perform_action(self, props):
        return None


class RecipeAction(Action):
    """ Recipe action """
    def __init__(self, args_dict):
        super().__init__(args_dict)
        self.args_dict = args_dict
        self.actions = {
            'conf': ConfAction,
            'preseed': PreseedAction,
            'apt': AptAction,
            'overlay': OverlayAction,
            'run': RunAction,
            'extra': ExtraAction,
            'downloads': DownloadsAction,
            'recipe': RecipeAction,
            'debos': DebosAction,
        }

    def create_action(self, action_type, args):
        """ Create a new action """
        try:
            return self.actions[action_type](args)
        except KeyError as exc:
            raise KeyError('Unknown action type!') from exc

    def _load_recipe(self, filename, substitutions=None):
        """ Load the yaml recipe """
        recipe_file = self.input_dir / filename
        full_yaml = load_yaml(recipe_file, substitutions)
        return full_yaml['recipe']

    def _working_dir(self, props):
        """ Define the recipe's working dir """
        if working_dir := props.get('working_dir'):
            self.input_dir = pl.Path(working_dir)

    def _get_args(self, props):
        """ Get input arguments """
        if working_dir := props.get('working_dir'):
            return dict(self.args_dict, input=working_dir)
        return dict(self.args_dict)

    def _perform_action(self, props):
        """ Perform all actions contained in the recipe """
        self._working_dir(props)
        recipe_filename =  props['recipe']
        substitutions = props.get('substitutions')
        recipe = self._load_recipe(recipe_filename, substitutions)
        args_dict = self._get_args(props)
        for action_props in recipe:
            action_type = action_props['action']
            action = self.create_action(action_type, args_dict)
            action.execute(action_props)
            self.result.extend(action.result)

    def get_result(self):
        """ Return results dictionary """
        return self.result
