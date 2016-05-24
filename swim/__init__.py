import platform
import os
import shutil
from glob import glob
import click
import subprocess

from swim.package import Package
from swim.builder import Builder



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
    builder = Builder(package)
    builder.build()


@click.command()
def test():
    if not os.path.exists('Package.swift'):
        raise click.ClickException('no Package.swift found')

    package = Package.open()
    builder = Builder(package)
    builder.build_tests()
    builder.run_tests()


cli.add_command(build)
cli.add_command(test)
cli.add_command(clean)
