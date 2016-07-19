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
        self.verbose = False

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

        has_main = len([s for s in sources if s.endswith('/main.swift')]) > 0
        if has_main:
            self.build_cli(package.name, sources, dependencies)
        else:
            self.build_library(package.name, sources, dependencies)

    def build_tests(self):
        package = self.package
        package_root = os.getcwd()
        self.build_package(package, package_root)

        download_dependencies(package.test_dependencies)
        dependencies = []
        for dependency in package.test_dependencies:
            path = path_for_dependency(dependency)

            os.chdir(path)
            sub_package = Package.open()
            os.chdir(os.path.join('..', '..'))

            self.build_package(sub_package, path)
            dependencies.append(sub_package)
        dependencies.append(package)

        for dependency in package.dependencies:
            path = path_for_dependency(dependency)

            os.chdir(path)
            sub_package = Package.open()
            os.chdir(os.path.join('..', '..'))

            dependencies.append(sub_package)

        sources = collect_sources(os.path.join(package_root, 'Tests'))

        has_main = len([s for s in sources if s.endswith('/main.swift')]) > 0
        if has_main:
            self.build_cli(package.name + 'Tests', sources, dependencies)
        else:
            raise Exception('Tests is missing a main.swift')

    def run_tests(self):
        os.environ['LD_LIBRARY_PATH'] = self.build_path
        runner = os.path.join(self.build_path, self.package.name + 'Tests')
        subprocess.check_call(runner)


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

        if self.verbose:
            print(' '.join(args + list(arguments)))

        subprocess.check_call(args + list(arguments))

    def build_cli(self, module, sources, dependencies):
        """
        Buils a command line tool.
        """

        args = [
            '-o', '.build/{}/{}'.format(self.configuration, module),
        ] + sources

        self.swiftc(module, dependencies, *args)

    def build_library(self, module, sources, dependencies):
        """
        Buils the module as a library.
        """

        if platform.system() == 'Darwin':
            libname = 'lib{}.dylib'.format(module)
        else:
            libname = 'lib{}.so'.format(module)

        args = [
            '-emit-module',
            '-emit-module-path', os.path.join(self.build_path, '{}.swiftmodule'.format(module)),
            '-emit-library',
            '-o', os.path.join(self.build_path, libname),
        ] + sources

        self.swiftc(module, dependencies, *args)


def collect_sources(path):
    return glob(os.path.join(path, '*.swift'))
