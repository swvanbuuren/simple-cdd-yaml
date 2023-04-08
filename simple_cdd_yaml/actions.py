""" Action handlers for Simple-cdd-yaml recipes """

import pathlib as pl
import tarfile
import re
import shutil
import textwrap
import yaml
import jinja2
from simple_cdd_yaml.yaml_loader import load_yaml


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

    def __init__(self, args):
        self.profile = args.profile
        self.output_dir = pl.Path(args.output)

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

    @staticmethod
    def _read_subst(filename, substitutions):
        """ Read string from file and perform jinja2 substitutions """
        with open(filename, mode='r', encoding='utf-8') as file:
            template = jinja2.Template(file.read())
        return template.render(substitutions)

    def _write_action(self, string, extension, directory='profiles',
                      no_duplicate=False):
        """ Append string to profile file """
        filename = self.profile + '.' + extension
        outpout_file = self.output_dir / directory / filename
        if no_duplicate and outpout_file.is_file():
            with open(outpout_file, mode='r', encoding='utf-8') as file:
                if string in file.read():
                    return
        with open(outpout_file, mode='a', encoding='utf-8') as file:
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
        return None


class PreseedAction(Action):
    """ Preseed action """
    def _perform_action(self, props):
        return self._read_subst(props['preconf'],
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
            if scripted:
                apt_install_script = self.packages_template.render(
                    description=description,
                    pkg_list=pkg_list)
                self._write_action(apt_install_script, extension='postinst')
                return None
            packages.insert(0, '# ' + description)
            return '\n'.join(packages) + '\n\n'
            # return self._pkg_dependencies(pkg_list, description)
        return None


class OverlayAction(Action):
    """ Overlay action """
    def __init__(self, args):
        super().__init__(args)
        self.overlay_template = jinja2.Template(OVERLAY_TEMPLATE_STR)

    def _perform_action(self, props):
        description = props.get('description', 'Overlay')
        user = props.get('user')
        overlay_name = props['source'].replace('/', '.')
        source_dir = pl.PurePath(pl.Path.cwd() / props['source'])
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
        return None


class ScriptAction(Action):
    """ Script action """
    action_out = 'postinst'
    def _perform_action(self, props):
        description = props.get('description', 'Script')
        script = self._read_subst(props['script'],
                                  props.get('substitutions', {}))
        script = re.sub(r'#!/bin/.*?sh\n', '', script)
        return f'\n# {description}\n{script}\n'


class RunAction(Action):
    """ Run action """
    action_out = 'postinst'

    def _perform_action(self, props):
        description = props.get('description', 'Run command')
        user = props.get('user')
        template = jinja2.Template(props['command'])
        command = template.render(props.get('substitutions', {}))
        if user:
            command = f"su - {user} << 'EOF'\n{command}\nEOF\n"
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


class RecipeAction(Action):
    """ Recipe action """
    def __init__(self, args):
        super().__init__(args)
        self.actions = {
            'conf': ConfAction(args),
            'preseed': PreseedAction(args),
            'apt': AptAction(args),
            'overlay': OverlayAction(args),
            'script': ScriptAction(args),
            'run': RunAction(args),
            'extra': ExtraAction(args),
            'downloads': DownloadsAction(args),
            'recipe': self,
        }

    @staticmethod
    def _load_recipe(file, substitutions=None):
        """ Load the yaml recipe """
        full_yaml = load_yaml(file, substitutions)
        return full_yaml['recipe']

    def _perform_action(self, props):
        recipe_file = props['recipe']
        substitutions = props.get('substitutions')
        recipe = self._load_recipe(recipe_file, substitutions)
        for action_props in recipe:
            action_type = action_props['action']
            try:
                action = self.actions[action_type]
            except KeyError as exc:
                raise KeyError('Unknown action type!') from exc
            action.execute(action_props)
        return None
