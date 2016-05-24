import platform
import os
import shutil
from glob import glob
import click
import subprocess

from swim.package import Package


def collect_sources(path):
    return glob(os.path.join(path, '*.swift'))


def swiftc_cli(module, configuration, sources):
    """
    Buils a command line tool.
    """

    args = [
        'swiftc',
        '-module-name', module,
        '-module-cache-path', '.build/{}/ModuleCache'.format(configuration),

    ]

    if platform.system() == 'Darwin':
        args += [
            '-target', 'x86_64-apple-macosx10.10',
            '-sdk', '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk',
        ]

    args += [
        '-o', '.build/{}/{}'.format(configuration, module),
    ]

    subprocess.check_call(args + sources)


@click.group()
def cli():
    pass


@click.command()
def clean():
    if os.path.exists('.build'):
        shutil.rmtree('.build')


@click.command()
def build():
    if not os.path.exists('Package.swift'):
        raise click.ClickException('no Package.swift found')

    package = Package.open()

    sources = collect_sources('Sources')
    configuration = 'debug'

    has_main = len([s for s in sources if s.endswith('/main.swift')]) > 0
    if has_main:
        swiftc_cli(package.name, configuration, sources)
    else:
        raise click.ClickException('swim only supports CLI tools')


cli.add_command(build)
cli.add_command(clean)
