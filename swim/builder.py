import os
from glob import glob
import platform
import subprocess

from package import Package
from downloader import path_for_dependency, download_dependencies


class Builder(object):
    def __init__(self, package, configuration='debug'):
        self.package = package
        self.configuration = configuration
        self.build_path = os.path.join('.build', configuration)

    def build(self):
        self.build_package(self.package, os.getcwd())

    def build_package(self, package, package_root):
        download_dependencies(package.dependencies)
        dependencies = []
        for dependency in package.dependencies:
            path = path_for_dependency(dependency)

            os.chdir(path)
            sub_package = Package.open()
            os.chdir(os.path.join('..', '..'))

            self.build_package(sub_package, path)
            dependencies.append(sub_package)


        sources = collect_sources(os.path.join(package_root, 'Sources'))
        configuration = 'debug'

        has_main = len([s for s in sources if s.endswith('/main.swift')]) > 0
        if has_main:
            self.build_cli(package.name, sources, dependencies)
        else:
            self.build_library(package.name, sources, dependencies)

    def swiftc(self, module, dependencies, *arguments):
        args = [
            'swiftc',
            '-module-name', module,
            '-module-cache-path', os.path.join(self.build_path, 'ModuleCache'),
            '-I', self.build_path,
            '-L', self.build_path,
        ]

        if platform.system() == 'Darwin':
            args += [
                '-target', 'x86_64-apple-macosx10.10',
                '-sdk', '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.11.sdk',
            ]

        if self.configuration == 'debug':
            args.append('-g')
            args.append('-Onone')
            args.append('-enable-testing')

        args += ['-l{}'.format(d.name) for d in dependencies]

        print(args + list(arguments))
        subprocess.check_call(args + list(arguments))

    def build_cli(self, module, sources, dependencies):
        """
        Buils a command line tool.
        """

        args = [
            '-o', '.build/{}/{}'.format(configuration, module),
        ] + sources

        self.swiftc(module, dependencies, *args)

    def build_library(self, module, sources, dependencies):
        """
        Buils the module as a library.
        """

        args = [
            '-emit-module',
            '-emit-module-path', self.build_path + '/',
            '-emit-library',
            '-o', os.path.join(self.build_path, 'lib{}.dylib'.format(module)),
        ] + sources

        self.swiftc(module, dependencies, *args)


def collect_sources(path):
    return glob(os.path.join(path, '*.swift'))
