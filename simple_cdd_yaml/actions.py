""" Action handlers for Simple-cdd-yaml recipes """

import copy
import pathlib as pl
import tarfile
import re
import shutil
import textwrap
import uuid
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

SCRIPT_TEMPLATE_DICT = \
    {
         'action': 'run',
         'description': 'Script action',
         'script': 'scripts/script.sh'
    }

COMMAND_TEMPLATE_DICT = \
    {
         'action': 'run',
         'description': 'Command action',
         'chroot': False,
         'command': ''
    }


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
        self.result = {
            'architecture': '',
            'chroot_default': False,
            'actions': [], 
            'pre-actions': [], 
            'post-actions': [],
        }

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

    def perform_action(self, props):
        """ Perform the action specific tasks and return result """
        raise NotImplementedError('Action is an abstract base class!')

    def perform_debos_action(self, props):
        """ Process debos action specific tasks and return result """
        raise NotImplementedError('Action is an abstract base class!')

    def execute(self, props):
        """ Execute an action """
        self._action_inform(props)
        if self.debos:
            result = self.perform_debos_action(props)
        else:
            result = self.perform_action(props)
        if result:
            if not self.action_out:
                self.action_out = props['action']
            self._write_action(result, self.action_out)

    def append_result(self, new_result: dict, key='actions'):
        """ Append a new result to the result list """
        added_result = copy.deepcopy(new_result)
        self.result[key].append(added_result)

    def extend_result(self, new_result: dict, key='actions'):
        """ Append a new result to the result list """
        added_result = copy.deepcopy(new_result)
        self.result[key].extend(added_result)

    def prepend_result(self, new_result: dict, key='actions'):
        """ Prepend a new result to the result list """
        added_result = copy.deepcopy(new_result)
        self.result[key].insert(0, added_result)

    def combine_results(self, result):
        """ Combine two result sets """
        for key in ('actions', 'pre-actions', 'post-actions'):
            self.result[key].extend(result[key])
        for option in ('architecture', 'chroot_default'):
            if result.get(option):
                self.result[option] = result[option]

    def unique_filename(self, base='script', ext='sh', description=None):
        """ Create a name from description or using uuid """
        name = base + '_'
        if description:
            name += description.lower()
        else:
            name += str(uuid.uuid4().hex)
        return "".join([x if x.isalnum() else "_" for x in name]) + '.' + ext


class ConfAction(Action):
    """ Conf action """
    def perform_action(self, props):
        description = props.get('description', 'Conf settings')
        conf_str = f'# {description}\n'
        if variables := props.get('variables'):
            for var, value in variables.items():
                conf_str += f'{var}="{value.rstrip()}"\n'
        if env_variables := props.get('env_variables'):
            for var, value in env_variables.items():
                conf_str += f'export {var}="{value.rstrip()}"\n'
        if variables or env_variables:
            return conf_str
        return None

    def perform_debos_action(self, props):
        return None


class PreseedAction(Action):
    """ Preseed action """
    def perform_action(self, props):
        return self._read_substitute(props['preconf'],
                                     props.get('variables', {}))

    def perform_debos_action(self, props):
        return None


class AptAction(Action):
    """ Apt action """
    action_out = 'packages'

    def __init__(self, args):
        super().__init__(args)
        self.packages_template = jinja2.Template(PACKAGES_TEMPLATE_STR)
        self.all_pkgs = set()

    def perform_action(self, props):
        """ Process APT action """
        if packages := props.get('packages'):
            pkg_list = ' '.join(packages)
            self._print(pkg_list, header='Requested packages:')
            description = props.get('description', 'Install packages')
            if props.get('scripted', False):
                apt_install_script = self.packages_template.render(
                    description=description,
                    pkg_list=pkg_list)
                self._write_action(apt_install_script, extension='postinst')
                return None
            packages.insert(0, '# ' + description)
            return '\n'.join(packages) + '\n\n'
        return None

    def perform_debos_action(self, props):
        self.append_result(props)


class OverlayAction(Action):
    """ Overlay action """
    def __init__(self, args):
        super().__init__(args)
        self.overlay_template = jinja2.Template(OVERLAY_TEMPLATE_STR)

    def source(self, props):
        source = props['source']
        if source.startswith('/'):
            return pl.PurePath(source)
        return pl.PurePath(self.input_dir / source)

    def overlay_name(self, props):
        overlay_name = props['source'].replace('/', '.')
        if user := props.get('user'):
            return f'{overlay_name}.{user}'
        return overlay_name

    def tar_filter(self, props):
        if user := props.get('user'):
            return OwnerTarFilter(user=user).tar_filter
        return None

    def destination(self, props):
        """ If destination is provided, this overrules the user setting """
        if dest := props.get('destination'):
            return dest
        if user := props.get('user'):
            if user == 'root':
                return '/root/'
            return f'/home/{user}/'
        return '/'

    def compress_overlay(self, props, output_dir):
        """ Compress overlay into tarball """
        name = self.overlay_name(props)
        filename = f'{self.profile}.{name}.tar.gz'
        src = self.source(props)
        tfilter = self.tar_filter(props)
        with tarfile.open(output_dir / filename, "w:gz") as tar:
            tar.add(src, arcname='', filter=tfilter)
        dest = self.destination(props)
        return filename, dest

    def perform_action(self, props):
        output_dir = self.output_dir / 'extra'
        filename, destination = self.compress_overlay(props, output_dir)
        self._write_action(f'extra/{filename}\n', extension='extra',
                           no_duplicate=True)
        extract_commands = self.overlay_template.render(
            description=props.get('description', 'Overlay'),
            overlay=filename,
            destination=destination,
        )
        self._write_action(extract_commands, extension='postinst')

    def perform_debos_action(self, props):
        output_dir = self.debos_output_dir / 'overlays'
        filename, destination = self.compress_overlay(props, output_dir)
        debos_action = dict(COMMAND_TEMPLATE_DICT,
            description=props.get('description', 'Overlay'),
            command=f'tar -xf $ARTIFACTDIR/overlays/{filename} -C $ROOTDIR{destination}'
        )
        self.append_result(debos_action)


class RunAction(Action):
    """ Run action """
    action_out = 'postinst'

    def script(self, props):
        """ Shell commands to run a script """
        description = props.get('description', 'Run script')
        script = self._read_substitute(props['script'],
                                       props.get('variables', {}))
        script = re.sub(r'#!/bin/.*?sh\n', '', script)
        return f'\n# {description}\n{script}\n'

    def command(self, props):
        """ Shell code to run a command """
        description = props.get('description', 'Run command')
        template = jinja2.Template(props['command'])
        command = template.render(props.get('variables', {}))
        if user:= props.get('user'):
            command = f"su - {user} << 'EOF'\n{command}\nEOF"
        return f'\n# {description}\n{command}\n'

    def create_run_script(self, props):
        """ Create script from run action """
        if all(x in props for x in ['script', 'command']):
            raise ActionError('Too many keywords: script and command found!')
        if 'script' in props:
            return self.script(props)
        if 'command' in props:
            return self.command(props)
        raise ActionError('Missing script or command keyword!')

    def perform_action(self, props):
        return self.create_run_script(props)

    def perform_debos_action(self, props):
        if 'postprocess' in props:
            self.append_result(props)
            return
        script_str = '#!/bin/sh' + self.create_run_script(props)
        filename = self.unique_filename(description=props.get('description'))
        output_file = self.debos_output_dir / 'scripts' / filename
        with open(output_file, mode='w', encoding='utf-8') as file:
            file.write(script_str)
        debos_action = dict(SCRIPT_TEMPLATE_DICT,
            description=props.get('description', 'Script'),
            script='scripts/'+filename,
        )
        self.append_result(debos_action)


class ExtraAction(Action):
    """ Extra action """
    def perform_action(self, props):
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

    def perform_debos_action(self, props):
        return None


class DownloadsAction(Action):
    """ Downloads action """
    def perform_action(self, props):
        description = props.get('description', 'Additional packages')
        pkg_list = props['packages']
        self._print(' '.join(pkg_list), header='Extra packages:')
        downloads_pkg_list = '\n'.join(pkg_list)
        return f'# {description}\n{downloads_pkg_list}\n'

    def perform_debos_action(self, props):
        return None

class DebosAction(Action):
    """ Debos action """
    def __init__(self, args_dict):
        super().__init__(args_dict)
        self.args_dict = args_dict
        self.actions = {
            'overlay': OverlayAction,
            'run': RunAction,
        }

    def create_action(self, action_type, args):
        """ Create a new action """
        try:
            return self.actions[action_type](args)
        except KeyError:
            return None

    def process_actions(self, action_list, action_key):
        """ Process given list of actions """
        for action_props in action_list:
            action_type = action_props['action']
            action = self.create_action(action_type, self.args_dict)
            if action:
                action.execute(action_props)
                self.extend_result(action.result['actions'], key=action_key)
            else:
                self.append_result(action_props, key=action_key)

    def perform_action(self, props):
        return None

    def perform_debos_action(self, props):
        for option in ('architecture', 'chroot_default'):
            self.result[option] = props[option]    
        for debos_action_type in ('pre-actions', 'post-actions'):
            self.process_actions(props[debos_action_type], debos_action_type)


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
        return full_yaml['actions']

    def _working_dir(self, props):
        """ Define the recipe's working dir """
        if working_dir := props.get('working_dir'):
            self.input_dir = pl.Path(working_dir)

    def _get_args(self, props):
        """ Get input arguments """
        if working_dir := props.get('working_dir'):
            return dict(self.args_dict, input=working_dir)
        return dict(self.args_dict)

    def process_actions(self, props):
        """ Perform all actions contained in the recipe """
        self._working_dir(props)
        recipe_filename =  props['recipe']
        substitutions = props.get('variables')
        recipe = self._load_recipe(recipe_filename, substitutions)
        args_dict = self._get_args(props)
        for action_props in recipe:
            action_type = action_props['action']
            action = self.create_action(action_type, args_dict)
            action.execute(action_props)
            self.combine_results(action.result)

    def perform_debos_action(self, props):
        self.process_actions(props)

    def perform_action(self, props):
        self.process_actions(props)

    def get_result(self):
        """ Return results dictionary """
        return self.result
