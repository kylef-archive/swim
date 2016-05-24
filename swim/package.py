import os
import tempfile
import json
from subprocess import Popen, PIPE


class Dependency(object):
    @classmethod
    def fromjson(cls, json):
        return cls(json['url'])

    def __init__(self, url):
        self.url = url


class Package(object):
    @classmethod
    def open(cls):
        if os.stat('Package.swift').st_size == 0:
            name = os.path.basename(os.getcwd())
            return cls(name=name)

        with open('Package.swift') as fp:
            package_source = fp.read().replace('import PackageDescription', '')

        file_dirname = os.path.dirname(os.path.abspath(__file__))
        description = os.path.join(file_dirname, 'PackageDescription.swift')

        with open(description) as fp:
            contents = fp.read().replace('// package', package_source)

        with tempfile.NamedTemporaryFile() as fp:
            fp.write(contents)
            fp.flush()

            process = Popen(['swift', fp.name], stdout=PIPE, stderr=PIPE)
            output, err = process.communicate()
            if process.returncode != 0:
                raise Exception('Problem Building Package: {}'.format(err))

            package = json.loads(output)

        dependencies = [Dependency.fromjson(x) for x in package['dependencies']]
        test_dependencies = [Dependency.fromjson(x) for x in package['test_dependencies']]

        return cls(name=package['name'],
                   dependencies=dependencies,
                   test_dependencies=test_dependencies)

    def __init__(self, name, dependencies=None, test_dependencies=None):
        self.name = name
        self.dependencies = dependencies or []
        self.test_dependencies = test_dependencies or []

    def __str__(self):
        return self.name
