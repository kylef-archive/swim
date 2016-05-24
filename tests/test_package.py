import os
import unittest

from swim.package import Package


class PackageTest(unittest.TestCase):
    def test_package_name(self):
        package = Package(name='hpack')
        self.assertEqual(package.name, 'hpack')

    def test_open_package_name(self):
        with chdir('tests/fixtures/hpack-name'):
            package = Package.open()

        self.assertEqual(package.name, 'hpack')

    def test_open_package_dependencies(self):
        with chdir('tests/fixtures/stencil'):
            package = Package.open()

        self.assertEqual(package.name, 'Stencil')
        self.assertEqual(len(package.dependencies), 1)
        self.assertEqual(len(package.test_dependencies), 1)
        self.assertEqual(package.dependencies[0].url,
            'https://github.com/kylef/PathKit.git')
        self.assertEqual(package.test_dependencies[0].url,
            'https://github.com/kylef/spectre-build')


class chdir(object):
    def __init__(self, directory):
        self.directory = directory

    def __enter__(self):
        self.working_directory = os.getcwd()
        os.chdir(self.directory)
        return self.directory

    def __exit__(self, typ, value, traceback):
        os.chdir(self.working_directory)
